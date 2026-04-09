# 部署原则
+ **命名**
    - 公共模型：模型名称
    - 测试模型：公共模型加尾缀（3fs, mtp, 8tp）。纯测试、验收用，不允许线上接流
+ **冗余**
    - 3个集群：2 份 replica - 1 份 gray（金丝雀）；测试模型不接流，不做要求

# 资源预估
| **<font style="color:rgb(31, 31, 31);">符号</font>** | **<font style="color:rgb(31, 31, 31);">含义</font>** | **<font style="color:rgb(31, 31, 31);">Config 对应字段</font>** | **<font style="color:rgb(31, 31, 31);">典型值 (GLM-4-355B)</font>** |
| --- | --- | --- | --- |
| <font style="color:rgb(31, 31, 31);"></font>$ h  $ | <font style="color:rgb(31, 31, 31);">隐藏层维度</font> | `<font style="color:rgb(68, 71, 70);">hidden_size</font>` | <font style="color:rgb(31, 31, 31);">5120</font> |
| <font style="color:rgb(31, 31, 31);"></font>$ L $ | <font style="color:rgb(31, 31, 31);">总层数</font> | `<font style="color:rgb(68, 71, 70);">num_hidden_layers</font>` | <font style="color:rgb(31, 31, 31);">92</font> |
| <font style="color:rgb(31, 31, 31);"></font>$ L_{dense}  $ | <font style="color:rgb(31, 31, 31);">稠密层数</font> | `<font style="color:rgb(68, 71, 70);">first_k_dense_replace</font>` | <font style="color:rgb(31, 31, 31);">3</font> |
| <font style="color:rgb(31, 31, 31);"></font>$ L_{moe} $ | <font style="color:rgb(31, 31, 31);">MoE 层数</font> | <font style="color:rgb(31, 31, 31);"></font>$ L - L_{dense}  $ | <font style="color:rgb(31, 31, 31);">89</font> |
| <font style="color:rgb(31, 31, 31);"></font>$ V $ | <font style="color:rgb(31, 31, 31);">词表大小</font> | `<font style="color:rgb(68, 71, 70);">vocab_size</font>` | <font style="color:rgb(31, 31, 31);">151552</font> |
| <font style="color:rgb(31, 31, 31);"></font>$ P_w $ | <font style="color:rgb(31, 31, 31);">权重精度(字节)</font> | <font style="color:rgb(31, 31, 31);">(FP16=2, FP8=1, Int4=0.5)</font> | <font style="color:rgb(31, 31, 31);">1 (FP8)</font> |
| $ n_{kv} $ | <font style="color:rgb(31, 31, 31);">KV Heads数量</font> | `num_key_value_heads` | <font style="color:rgb(31, 31, 31);">8</font> |
| <font style="color:rgb(31, 31, 31);"></font>$ d_{head} $ | <font style="color:rgb(31, 31, 31);">维度</font> | `head_dim` | <font style="color:rgb(31, 31, 31);">128</font> |


## 显存
TL; DR：直接看 prefill 机器的 engine.log，关键词：CacheConfig，算好了 KV Cache 的存储大小及最大输入 Token 长度。

$ 显存 = 模型权重 + RESERVER\_RUNTIME\_MEM\_MB(WARM\_UP) + KV Cache + DEVICE\_RESERVE\_MEMORY\_BYTES $

+ 模型权重：大小固定，但可以通过 EP 和 TP 分散到多张卡上。TP 会切分所有层，而 EP 只切分 MoE 的路由专家层（稠密层会被复制）
+ device：为硬件预留的，例如通信
+ runtime：rtp-llm 维持运行所需要的存储大小
+ KV Cache：其余空闲区域

### 模型权重
$ \text{Total} = M_{vocab} + M_{attn} + M_{dense} + M_{shared} + \mathbf{M_{routed}} $

1. 词表与输出层 (Embeddings)：通常这部分随 TP (Tensor Parallel) 切分，但在某些框架中为了减少通信可能不切分。此处按标准 TP 切分计算。

$ M_{vocab} = \frac{2 \times V \times h \times P_w}{TP} $$ = 2 \times \text{vocab\_size} \times \text{hidden\_size} \times \text{prec} \div \text{TP} $

注：乘 2 是因为包含 Input Embedding 和 Output Head (当 `tie_word_embeddings`=False 时)。



2. Attention 机制 (所有层)：Attention 层存在于每一层（无论是 Dense 还是 MoE 层），通常由 TP 切分。

$ M_{attn} = \frac{L \times h \times d_{head} \times (N_q + 2N_{kv}) \times P_w}{TP} $$ = \text{num\_hidden\_layers} \times \text{hidden\_size} \times \text{head\_dim} \times (\text{num\_attention\_heads} + 2 \times \text{num\_key\_value\_heads}) \times \text{prec} \div \text{TP} $注：$ 2 \times N_{kv} $代表 K 和 V 矩阵；$ N_q
 $代表 Q 和 O 矩阵（O 的形状转置后参数量等同于 Q）。



3. FFN: 稠密层部分 (Dense Layers)：仅指模型开头的前 $ L_{dense} $ 层（通常前 3 层）。这部分由 TP 切分。

$ M_{dense} = \frac{L_{dense} \times 3 \times h \times d_{ff} \times P_w}{TP} $$ = \text{first\_k\_dense\_replace} \times 3 \times \text{hidden\_size} \times \text{intermediate\_size} \times \text{prec} \div \text{TP} $

注：乘 3 代表 SwiGLU 结构的三个矩阵：Gate, Up, Down。



4. MoE: 共享专家 (Shared Experts)：GLM-4 在 MoE 层中保留了一个“共享专家”（通常是一个标准的 Dense FFN）。这部分逻辑上由 TP 切分。

$ M_{shared} = \frac{L_{moe} \times N_{shared} \times 3 \times h \times d_{ff} \times P_w}{TP} $$ = (L - L_{dense}) \times \text{n\_shared\_experts} \times 3 \times \text{hidden\_size} \times \text{intermediate\_size} \times \text{prec} \div \text{TP} $

注：Shared Expert 通常使用大的 `intermediate_size` (12288)，而非小的 MoE 维度。



5. MoE: 路由专家 (Routed Experts) —— 显存大头：这是 MoE 的核心，由 EP (Expert Parallel) 切分。如果你没开 EP (EP=1)，则由 TP 切分；如果开了 EP，则除以 EP。

$ M_{routed} = \frac{L_{moe} \times N_{exp} \times 3 \times h \times d_{moe} \times P_w}{EP} $$ = (L - L_{dense}) \times \text{n\_routed\_experts} \times 3 \times \text{hidden\_size} \times \text{moe\_intermediate\_size} \times \text{prec} \div \text{EP} $

**重要**：这里使用的是 `moe_intermediate_size` (通常较小，如 1536)。分母是 EP。

### KV Cache
1. KV Cache 存储大小姑且叫 kv_cache_size。来源：[FT框架知识学习](https://aliyuque.antfin.com/zhoumingxian.zmx/nk5t6h/np44nzggetf7vruv)



2. 单个 Token 所占显存大小，姑且叫 one_token_cache。来源：[deepseek技术解读(1)-彻底理解MLA（Multi-Head Latent Attention）](https://mp.weixin.qq.com/s?__biz=MzU0MDQ1NjAzNg==&mid=2247587790&idx=1&sn=bba1f7b1ab1a385bddca8d054affe410&poc_token=HO6avmij2736z77lGf1v2ce2C1oaZqMAgMyyH5jH)

$ \text{KV}_{per\_token} = \frac{2 \times L \times n_{kv} \times d_{head} \times P_{kv}}{TP} 
\newline =
2 * \text{num_hidden_layers} \times \text{num_key_value_heads} \times \text{head_dim} \times \text{kvcache_dtype_byte} \div \text{TP} $

```python
# take GLM-4.6 as example
hidden_size = 5120
num_attention_heads = 96
num_hidden_layers = 92
head_dim = 128
num_key_value_heads = 8  # if not grouped kv cache, num_key_value_heads equals num_attention_heads
kvcache_dtype_byte = 2  # bf16/fp16 -> 2, fp8/int8 -> 1
tp_size = 8
# k cache and v cache
one_token_cache = 2 * num_hidden_layers * num_key_value_heads * head_dim * kvcache_dtype_byte / tp_size
```

[https://huggingface.co/docs/transformers/en/main_classes/configuration](https://huggingface.co/docs/transformers/en/main_classes/configuration)

3. kv_cache_size / one_token_cache = 最大输入 token

```python
# cpp backend 中，AttentionConfigs 初始化还要根据 TP 并行再计算
head_num = head_num_ / tp_size_
kv_head_num = kv_head_num_ / tp_size_
# 不同的模型也会有不同的实现，例如如下为 qwen_v2 的配置读取方式 
size_per_head = config_json.get("head_dim") if "head_dim" in config_json else config_json["hidden_size"]
```

注：实际线上的 runtime 分配 Cache 的时候计算公式如下：

```cpp
auto v_output = allocateBuffer(
    {params.input.type(), {batch_size, kv_head_num, seq_len_with_prefix, size_per_head}, AllocationType::DEVICE},
    {"v_output"});
```

# 故障恢复
场景分类：

+ 资源水位异常
    - 水位高：检查业务调用量、检查资源余量
        * 方案：扩容 or 限流
+ 请求异常
    - 大量错误：429（同水位高）
        * 其他：根据错误码手册进行定位
    - 延迟升高：检查输入 TPM、QPS 上涨情况
        * 方案：扩容 or 限流
    - 少量异常
        * 看监控+日志，检查主要错误码、原因，及是否存在 ip 聚集问题

总结一下恢复手段：**扩容**、**限流**。目前全人工，未来探索自动化（HPA）、自适应过载保护。

[大模型可观测1-5-10：发现、定位、恢复的三层能力建设](https://mp.weixin.qq.com/s/aUlUrYjXsQPhZBND8jCnZA)


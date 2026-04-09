[CUDA C 编程引言——并行计算](https://zhuanlan.zhihu.com/p/21259313375)

# CUDA编程模型概述
CUDA C是一种专为NVIDIA GPU设计的编译型语言。与之类似的异构计算标准是OpenCL。主要区别在于生态和编译模型：

+ CUDA：是NVIDIA的私有生态系统，编译器在开发阶段将CUDA C++代码（包括主机端和设备端）编译好。这提供了高度的优化和成熟的工具链。
+ OpenCL：是一个开放的行业标准，支持不同厂商的硬件（如AMD、Intel、NVIDIA的GPU，以及FPGA等）。它的设备内核代码通常是在应用程序运行时，由驱动程序根据当前硬件进行即时编译（JIT）。这种方式提供了跨平台兼容性，但开发体验和极致性能优化通常不如CUDA直接。

编程的抽象层级如下：  
<img src="https://intranetproxy.alipay.com/skylark/lark/0/2025/png/180556543/1761300026849-795063d3-6b7f-4cc0-8ea4-29517565b269.png" width="1596" title="" crop="0,0,1,1" id="iXa0F" class="ne-image">  
其中Communication Abstraction是编程模型和编译器、库函数之间的分界线。简单来说，编程模型界定了以下几个问题：

+ **如何看待计算**？是单个执行单元（线程），还是成千上万个可以同时执行的任务？
+ **如何组织代码**？你的代码单元是什么？是函数，是对象，还是可以并行执行的“内核”？
+ **如何管理数据**？数据存放在哪里？所有计算单元都能访问所有数据吗？还是有不同层级、不同访问权限的内存？

CUDA编程模型的核心组成部分：

1. **线程管理**：通过Grid -> Block -> Thread的三级结构来组织数以万计的线程。这使得并行任务的划分和扩展变得简单。Block内的线程可以高效协作，Block间的独立性保证了大规模并行。
2. **内存管理**：提供了包括全局内存、共享内存、本地内存等在内的多层级内存。高性能编程的关键在于理解并善用这些不同速度和作用域的内存，尤其是利用高速的共享内存来减少对慢速全局内存的访问。
3. **核函数**：程序由运行在CPU上的主机代码和运行在GPU上的设备代码（内核）组成。主机负责流程控制和数据准备，并异步地在设备上启动计算任务，从而实现CPU和GPU的协同工作。
4. **流**。

掌握CUDA编程，本质上就是学习如何运用这一套模型，将你的问题“翻译”成GPU能够理解和高效执行的并行形式。

以上这些理论同时也适用于其他非CPU+GPU异构的组合。

# CUDA编程思路
GPU编程跟我们已知的CPU编程的不同之处在于，我们是在思考GPU架构下的几个特有功能：

+ **在GPU的多层结构上组织线程**
+ **在GPU的多层结构上组织内存**

其实说白了也就是对内存和线程的控制。如果**多个线程重复计算同一块数据，那就是浪费时间**，所以要让多线程按照设计处理到不同的数据，也因此我们一个唯一标识来确定每个线程。

宏观上可以从以下几个层次完成CUDA应用开发：

1. **领域层**：识别问题中哪些部分可以并行。核心是分析计算任务，找出数据无关或依赖关系简单的密集型计算部分（例如大规模的向量加法、矩阵乘法）。
2. **逻辑层**：设计并行算法。这里需要使用CUDA的编程模型来组织并行任务。核心是思考如何将数据和计算映射到Grid、Block和Thread的层次结构上，如何设计线程协作（使用共享内存、同步）来高效完成任务。这一层是并行思维的体现。
3. **硬件层**（Hardware Layer）：将逻辑设计映射到物理硬件。虽然程序员不直接控制，但理解这一层有助于写出高性能代码。例如，理解Block如何被调度到流式多处理器（SM）上，一个SM内的线程如何共享资源，这有助于我们设定合适的Block和Grid尺寸，以最大化硬件利用率。

<img src="https://intranetproxy.alipay.com/skylark/lark/0/2025/png/180556543/1761301378256-89a0da2d-bf58-4f28-b64b-de1492f44ae5.png" width="1684" title="" crop="0,0,1,1" id="QX6kp" class="ne-image">  


## 主机与设备的交互
一个异构环境，通常有多个CPU多个GPU，他们通过PCIe总线相互通信，也就意味着被PCIe总线分隔。所以区分两种设备的内存是有必要的：

+ 主机：CPU及其内存
+ 设备：GPU及其内存

注意：这两个内存从硬件到软件都是隔离的（CUDA 6.0 以后支持统一寻址），我们目前先不研究统一寻址，我们现在还是用内存来回拷贝的方法来编写调试程序，以巩固大家对两个内存隔离这个事实的理解。

一个完整的CUDA应用可能的执行顺序如下图：  
<img src="https://intranetproxy.alipay.com/skylark/lark/0/2025/png/180556543/1761301100386-5a6ced2e-f5e2-4b7f-95fd-15fc70e24a63.png" width="1748" title="" crop="0,0,1,1" id="GF9n8" class="ne-image">  
核函数被调用后控制权马上归还主机线程，主机不会等待设备完成核函数，也就是在第一个并行代码执行时，很有可能第二段host代码已经开始同步执行了。所有**CUDA核函数的启动都是异步的**，这点与C语言是完全不同的。

想要主机等待设备端执行可以用显式调用下面这个指令：

```
c cudaError_t cudaDeviceSynchronize(void);
```


对应的也有隐式方法，就是不明确说明主机要等待设备端，而是设备端不执行完，主机没办法进行，比如内存拷贝指令：

```
c cudaError_t cudaMemcpy(void* dst,const void * src, size_t count,cudaMemcpyKind kind);
```


当核函数启动后的主机的下一条指令就是从设备复制数据回主机端，那么主机端必须要等待设备端计算完成。

CUDA提供的API可以分配管理设备上的内存，也可以管理主机上的内存，主机上的传统标准库也能完成主机内存管理。

| 标准C函数 | CUDA C 函数 | 说明 |
| --- | --- | --- |
| malloc | cudaMalloc | 内存分配 |
| memcpy | cudaMemcpy | 内存复制。根据cudaMemcpyKind kind有不同的过程：<br/>+ cudaMemcpyHostToHost<br/>+ cudaMemcpyHostToDevice<br/>+ cudaMemcpyDeviceToHost<br/>+ cudaMemcpyDeviceToDevice |
| memset | cudaMemset | 内存设置 |
| free | cudaFree | 释放内存 |


如果函数执行成功，则会返回 cudaSuccess，否则返回 cudaErrorMemoryAllocation

可以使用下面的指令把错误代码翻译成详细信息：

```
plain char* cudaGetErrorString(cudaError_t error)
```


## 线程管理
CUDA的线程组织是一个清晰的三级层次结构：

Kernel Launch `<<<Grid, Block>>>` -> Grid -> Block -> Thread

+ 一次核函数调用会启动一个网格（Grid）。
+ 一个网格（Grid）由多个线程块（Block）组成。
+ 一个线程块（Block）由多个线程（Thread）组成。

这种结构可以总结为：用一个Grid的线程来执行整个任务，Grid被划分为多个Block独立执行子任务，每个Block内的线程则协作完成该子任务。  
<img src="https://intranetproxy.alipay.com/skylark/lark/0/2025/png/180556543/1761566995961-dd1a908b-3d63-4b26-8318-76a4fc0ec9dd.png" width="1406" title="" crop="0,0,1,1" id="t35ed" class="ne-image">

一个线程块block中的线程可以完成下述协作：

+ 同步
+ 共享内存

不同block内线程不能相互影响！他们是物理隔离的！

在 CUDA 中，`blockIdx`、`blockDim`、`threadIdx` 和 `gridDim` 这些术语指的是一个用于组织和识别 GPU 上线程（thread）与线程块（block）的层级结构。它们的核心区别在于，`blockIdx` 和 `threadIdx` 是位置索引，而 `blockDim` 和 `gridDim` 是维度尺寸。

| 术语 | 类别 | 范围 | 类型 | 值 |
| --- | --- | --- | --- | --- |
| `threadIdx` | 索引 | 线程块（block）局部 | uint3 | 特定线程（thread）在其线程块（block）内的唯一索引。例如，在一个包含 256 个线程（thread）的一维线程块（block）中，`threadIdx.x`的取值范围是 0 到 255。 |
| `blockIdx` | 索引 | 网格（grid）局部 | uint3 | 特定线程块（block）在整个线程块网格（grid）内的唯一索引。例如，在一个包含 16 个线程块（block）的一维网格（grid）中，`blockIdx.x`的取值范围是 0 到 15。 |
| `blockDim` | 尺寸 | 内核全局 | dim3/uint3 | 线程块（block）的尺寸（大小），指定了每个维度（`x`、`y`、`z`）中每个线程块（block）包含的线程（thread）数。这个值对于内核中的每个线程（thread）都是相同的。 |
| `gridDim` | 尺寸 | 内核全局 | dim3/uint3 | 网格（grid）的尺寸（大小），指定了每个维度（`x`、`y`、`z`）中线程块（block）的数量。这个值对于内核中的每个线程（thread）也是相同的。 |


  
为了获取整个网格（grid）中任何线程（thread）的唯一全局索引，必须结合使用 `blockIdx`、`blockDim` 和 `threadIdx` 变量。这是因为 `threadIdx` 的值在整个网格（grid）中不是唯一的；每当进入一个新的线程块（block）时，它的值都会重置。 

对于一维网格（grid）和线程块（block），全局线程（thread）索引（`tid`）的计算公式为：

```plain
tid = blockIdx.x * blockDim.x + threadIdx.x # 假设只有 x 轴
```

块（block）大小主要与**可利用的计算资源有关**，如寄存器共享内存。分成网格和块的方式可以使得我们的CUDA程序可以在任意的设备上执行。

```c
#include <cuda_runtime.h>
#include <stdio.h>
__global__ void checkIndex(void)
{
  printf("threadIdx:(%d,%d,%d) blockIdx:(%d,%d,%d) blockDim:(%d,%d,%d) "
         "gridDim:(%d,%d,%d)\n",
         threadIdx.x, threadIdx.y, threadIdx.z,
         blockIdx.x, blockIdx.y, blockIdx.z, blockDim.x, blockDim.y, blockDim.z,
         gridDim.x, gridDim.y, gridDim.z);
}
int main(int argc, char **argv)
{
  // 打印线程索引变量的类型信息
  printf("In main function:\n");
  printf("Size of dim3: %zu bytes\n", sizeof(dim3));

  int nElem = 6;
  dim3 block(3);
  dim3 grid((nElem + block.x - 1) / block.x);
  printf("grid.x %d grid.y %d grid.z %d\n", grid.x, grid.y, grid.z);
  printf("block.x %d block.y %d block.z %d\n", block.x, block.y, block.z);
  checkIndex<<<grid, block>>>();
  cudaDeviceReset();
  return 0;
}
```

```shell
$ ./check_index 
In main function:
Size of dim3: 12 bytes
grid.x 2 grid.y 1 grid.z 1
block.x 3 block.y 1 block.z 1
threadIdx:(0,0,0) blockIdx:(0,0,0) blockDim:(3,1,1) gridDim:(2,1,1)
threadIdx:(1,0,0) blockIdx:(0,0,0) blockDim:(3,1,1) gridDim:(2,1,1)
threadIdx:(2,0,0) blockIdx:(0,0,0) blockDim:(3,1,1) gridDim:(2,1,1)
threadIdx:(0,0,0) blockIdx:(1,0,0) blockDim:(3,1,1) gridDim:(2,1,1)
threadIdx:(1,0,0) blockIdx:(1,0,0) blockDim:(3,1,1) gridDim:(2,1,1)
threadIdx:(2,0,0) blockIdx:(1,0,0) blockDim:(3,1,1) gridDim:(2,1,1)
```

**注意：dim3 是主机端定义的，可见可修改。设备端在执行时会转成 uint3，可见但不可修改。**

## 核函数
核函数就是在CUDA模型上成千上万线程中运行的那段代码，这段代码在设备上被复制到大量线程里运行。用NVCC编译，产生的机器码是GPU的机器码，所以写CUDA程序就是写核函数。

### 启动核函数
启动核函数，通过的以下的ANSI C 扩展出的CUDA C指令：

```c kernel_name<<<grid, block>>>(argument list);
```

其标准C的原型就是C语言函数调用：

```
c function_name(argument list);
```


这个三个尖括号`<<<grid,block>>>`是对设备代码执行的线程结构的配置（或者称为对内核进行配置），也就是我们上一篇中提到的线程结构中的网格（grid）、块（block）。我们通过CUDA C内置的数据类型dim3的变量来配置grid和block。通过指定grid和block的维度，我们可以配置内核中线程的数量和线程的布局。

除了使用dim3类型的grid和block配置内核，也可以使用int类型的变量或者常量直接初始化：

```
c kernel_name<<<4, 8>>>(argument list); // 4 个块，每个块 8 个线程
```


上面这条指令的线程布局是：  
<img src="https://intranetproxy.alipay.com/skylark/lark/0/2025/png/180556543/1761643296983-7aa78ed4-bec0-488c-abc8-8c04567127ba.png" width="1626" title="" crop="0,0,1,1" id="u3441e70e" class="ne-image">

改变核函数的配置，会产生运行结果一样，但效率不同的代码：

```
c kernel_name<<<1,32>>>(argument list); // 1 个 block  kernel_name<<<32,1>>>(argument list); // 32 个 block
```

如果没有特殊逻辑，这两个核函数调用的执行结果应该一致，但其中一个的运行效率会较低，取决于具体逻辑。

### 编写核函数
声明核函数有一个比较模板化的方法，使用`__global__`限定符：

```
c __global__ void kernel_name(argument list);
```

CUDA C中还有一些在C中没有的限定符，如下：

| 限定符 | 执行 | 调用 | 备注 |
| --- | --- | --- | --- |
| __global__ | 设备端执行 | 可以从主机调用也可以从计算能力3以上的设备调用 | 必须有一个void的返回类型 |
| __device__ | 设备端执行 | 设备端调用 |  |
| __host__ | 主机端执行 | 主机调用 | 可以省略 |


而且这里有个特殊的情况就是有些函数可以同时定义为 device 和 host ，这种函数可以同时被设备和主机调用。主机端调用函数很正常，设备端调用函数与C语言一致，但是要声明成设备端代码，告诉nvcc编译成设备机器码。同时声明主机端+设备端函数，那么就要告诉编译器，生成两份不同设备的机器码。

**注意：声明和定义是不同的，这点CUDA与C语言是一致的**

<font style="color:rgb(85, 85, 85);background-color:rgba(255, 255, 255, 0.8);"></font>

Kernel核函数有以下限制：

1. 只能访问设备内存
2. 必须有void返回类型
3. 不支持可变数量的参数
4. 不支持静态变量
5. 异步行为

# CUDA执行模型（接近硬件）
CUDA执行模型揭示了GPU并行架构的抽象视图。了解CUDA的执行模型，可以帮助我们优化指令吞吐量、内存使用来获得极限速度。

限制内核性能的主要包括但不限于以下因素

+ 存储带宽
+ 计算资源
+ 指令和内存延迟

## GPU硬件组成
GPU架构是围绕一个流式多处理器（SM）的扩展阵列搭建的。通过复制这种结构来实现GPU的硬件并行。  
<img src="https://intranetproxy.alipay.com/skylark/lark/0/2025/png/180556543/1762173402892-be7cb4c8-da35-4893-8295-778ff4a52e2b.png" width="626" title="" crop="0,0,1,1" id="uaad2f88a" class="ne-image" style="color: rgb(85, 85, 85); font-size: 16px">

+ **SM**：GPU中每个SM都能支持数百个线程并发执行，每个GPU通常有多个SM，当一个核函数的grid被启动的时候，多个线程块会被同时分配给可用的SM上执行。在SM上同一个块内的多个线程进行线程级别并行，而单一线程内，指令则被指令级并行处理成流水线。

**注意**：当一个block被分配给一个SM后，他就只能在这个SM上执行了，不可能重新分配到其他SM上了，多个block可以被分配到同一个SM上。

+ **<font style="color:rgb(85, 85, 85);background-color:rgba(255, 255, 255, 0.8);">线程束</font>**<font style="color:rgb(85, 85, 85);background-color:rgba(255, 255, 255, 0.8);">：</font>CUDA 采用单指令多线程（SIMT）架构管理执行线程，不同设备有不同的线程束大小，但是到目前为止基本所有设备都是维持在32。也就是说每个SM上有多个block，一个block有多个线程，但是从机器的角度，在某时刻T，SM上只执行一个线程束，也就是32个线程在同时同步执行，线程束中的每个线程执行同一条指令，包括分支部分

## CUDA编程的组件与逻辑
下图从逻辑角度和硬件角度描述了CUDA编程模型的对应关系。

<img src="https://intranetproxy.alipay.com/skylark/lark/0/2025/png/180556543/1762173788834-0039bfe1-091d-4d10-bc7b-44deed8c05a6.png" width="827" title="" crop="0,0,1,1" id="u0445c701" class="ne-image">

SM中共享内存和寄存器是关键的资源，线程块中线程通过共享内存和寄存器相互通信协调。  
**寄存器和共享内存的分配可以严重影响性能！**

因为SM有限，虽然我们在编程模型层面看所有线程都是并行执行的，但是在微观上看，所有线程块也是分批次的在物理层面的机器上执行，线程块里不同的线程可能进度都不一样，但是同一个线程束内的线程拥有相同的进度。  
并行就会引起竞争，多线程以未定义的顺序访问同一个数据，就导致了不可预测的行为，CUDA只提供了一种块内同步的方式，块之间没办法同步！  
同一个SM上可以有不止一个常驻的线程束，有些在执行，有些在等待，他们之间状态的转换是不需要开销的。另外由于计算资源是在线程束之间分配的，且线程束的整个生命周期都在片上，所以线程束的上下文切换是非常快速的。

## 如何提升GPU性能
### 避免线程束分化
线程束被执行的时候会被分配给相同的指令，处理各自私有的数据。CUDA支持C语言的控制流，比如if…else, for ,while 等，但是如果一个线程束中的不同线程包含不同的控制条件，那么当我们执行到这个控制条件就会面临选择。

```
c if (con) {     //do something } else {     //do something }
```


GPU不像CPU有分支预测这种高级技术。假设这段代码是核函数的一部分，那么当一个线程束的32个线程执行这段代码的时候，如果其中16个执行if中的代码段，而另外16个执行else中的代码块，同一个线程束中的线程，执行不同的指令，这叫做**线程束的分化**。  
由于同一个线程束的时间必须同步，因此空闲的线程也必须等待还有任务的线程。也就是当一部分线程的con条件成立的时候，执行if块内的代码，另一部分线程con条件不成立则原地等待，直到其他线程也到达else再进行下一个指令。线程束分化会产生严重的性能下降。条件分支越多，并行性削弱越严重。如图：  
<img src="https://intranetproxy.alipay.com/skylark/lark/0/2025/png/180556543/1762175198995-ae9f0b0f-8297-4fca-851e-a0fd594ea2ed.png" width="2162" title="" crop="0,0,1,1" id="u5ecc667a" class="ne-image">

**注意**：线程束分化研究的是一个线程束中的线程，不同线程束中的分支互不影响。  
优化思路是避免线程束分化，这个思路是基于线程块中线程分配到的线程束是有规律的，而不是随机的。这就使得我们根据线程编号来设计分支是可以的。当一个线程束中所有的线程都执行if或者，都执行else时，不存在性能下降；只有当线程束内产生分支的时候，性能才会急剧下降：

```c
__global__ void mathKernel2(float *c)
{
	int tid = blockIdx.x* blockDim.x + threadIdx.x;
	float a = 0.0;
	float b = 0.0;
	if ((tid/warpSize) % 2 == 0)
	{
		a = 100.0f;
	}
	else
	{
		b = 200.0f;
	}
	c[tid] = a + b;
}
```

### 充分并行
#### 先介绍SM（Streaming Multiprocessor）的资源分配
每个SM上执行的基本单位是线程束，也就是说，单指令通过指令调度器广播给某线程束的全部线程，这些线程同一时刻执行同一命令。

而每个SM上有多少个线程束处于激活状态，取决于以下资源：

+ **程序计数器**
+ **寄存器**
+ **共享内存**

线程束一旦被激活来到片上，那么他就不会再离开SM直到执行结束。

每个SM都有32位的寄存器组，每个架构寄存器的数量不一样，其基本单元是寄存器文件，分配给每个线程。与此同时，还会分配固定数量的共享内存在线程块之间分配。具体怎么分配线程和线程束取决于SM中**可用的寄存器和共享内存**，以及**kernel需要的寄存器和共享内存大小**。打个比方，类似于工厂大小与工人数量之间的关系。

+ 小的线程块：每个线程块中线程太少，会在所有资源没用完就达到了线程束的最大要求
+ 大的线程块：每个线程块中太多线程，会导致每个SM中每个线程可用的硬件资源较少。

当SM内的资源没办法处理一个完整块，那么程序将无法启动。当SM要执行某个线程束的时候，执行的这个线程束叫做选定的线程束，准备要执行的叫符合条件的线程束，如果线程束不符合条件就是阻塞的线程束。  
满足下面的要求，线程束才算是符合条件的：

+ 32个CUDA核心可以用于执行
+ 执行所需要的资源全部就位

#### 隐藏延迟
**硬件利用率与常驻线程束直接相关**，因为我们可以通过大量的活跃的线程束切换来隐藏延迟。如果硬件中线程调度器每时每刻都有可用的线程束供其调度，避免空闲，就能达到计算资源的完全利用。该理念与CPU编程里的并行是一致的。但GPU编程有个专业术语叫做**隐藏延迟（Latency Hiding）**

与其他类型的编程相比，GPU的延迟隐藏及其重要，因为操作很多但很小。对于指令的延迟，通常分为两种：

+ **算术指令**：一个算术操作从开始到完成的时间。这个时间段内只有某些计算单元处于工作状态，而其他逻辑计算单元处于空闲，约 10~20 个时钟周期。隐藏是为了充分利用计算资源。
+ **内存指令**：当产生内存访问的时候，计算单元要等数据从内存拿到寄存器，这个周期是非常长的，约 400~800 个时钟周期。隐藏是为了充分利用内存带宽。

核心思想就是，但凡执行陷入等待，立刻换入其他准备好执行的线程束执行。

> Latency hiding is a strategy to mask long-latency operations by [running many of them concurrently](https://modal.com/gpu-glossary/perf/littles-law).
>
> Performant GPU programs hide latency by interleaving the execution of many [threads](https://modal.com/gpu-glossary/device-software/thread). This allows programs to maintain high throughput despite long instruction latencies. When one [warp stalls](https://modal.com/gpu-glossary/perf/warp-execution-state) on a slow memory operation, the GPU immediately switches to execute instructions from another [eligible warp](https://modal.com/gpu-glossary/perf/warp-execution-state).
>
> - "[What is latency hiding?](https://modal.com/gpu-glossary/perf/latency-hiding)"
>

为保证最小化延迟，所需线程束的计算公式：所需线程束=延迟×吞吐量。

+ 假如吞吐量等于最大带宽，得到的就是为达到硬件性能上限所需线程束。
+ 延迟是单位时间内处理的数据量，即带宽除以时钟周期。

为充分隐藏SM延迟，所需线程数的下界：SM的计算核心数乘以单条指令的延迟。比如32个单精度浮点计算器，每次计算延迟20个时钟周期，那么我需要最少 32x20 =640 个线程使设备处于忙碌状态。  
  


另外有两种方法可以提高并行：

+ 指令级并行(ILP): 并行执行线程中的多个指令
+ 线程级并行(TLP): 并行执行多个符合条件的线程

  
[CUDA 编程手册系列第五章: 性能指南](https://developer.nvidia.com/zh-cn/blog/cuda-performance-guide-cn/)

#### 指标与性能
+ kernel代码直接影响执行效率
+ 大部分情况，单一指标不能优化出最优性能：
    - 多个指标对执行效率有贡献，例如 Achieved Occupancy、Throughput，“速度”最快的不一定每个指标都高，需要平衡和取舍
    - grid和block的尺寸为调节性能提供了不错的抓手（不同尺寸多尝试、各种指标多分析）

[Nsight Compute CLI 和 nprof 的指标映射](https://docs.nvidia.com/nsight-compute/2019.5/NsightComputeCli/index.html#nvprof-metric-comparison)

### 展开循环
for循环算分支语句：

```c
for (int i = 0; i < tid; i++)
{
    // to do something
}
```

如果上面这段代码出现在内核中，就会有分支，因为一个线程束第一个线程和最后一个线程tid相差32（如果线程束大小是32的话） 那么每个线程执行的时候，for循环终止时完成的计算量都不同，这就有人要等待，这也就产生了分支。

循环展开就是把循环通过迭代做的事情直接手写在代码里。

在CUDA中展开循环的目的还是那两个：

1. 减少指令消耗
2. 增加更多的独立调度指令

### 动态并行
kernel中启动kernel，和cpu并行中有一个相似的概念，就是父线程和子线程。但是到了GPU，父子关系更多了：比如父网格、父线程块、父线程，对应的子网格、子线程块、子线程。子网格被父线程启动，且必须在对应的父线程、父线程块、父网格结束之前结束。所有的子网格结束后，父线程、父线程块、父网格才会结束。

<img src="https://intranetproxy.alipay.com/skylark/lark/0/2025/png/180556543/1763039758601-9399ff3f-73b6-4696-91f6-3c8af71e799d.png" width="815" title="" crop="0,0,1,1" id="u058f174f" class="ne-image">

动态并行的内存竞争主要的有下面几点：

1. 父网格和子网格共享相同的全局和常量内存。
2. 父网格子网格有不同的局部内存
3. 有了子网格和父网格间的弱一致性作为保证，父网格和子网格可以对全局内存并发存取。
4. 有两个时刻父网格和子网格所见内存一致：子网格启动的时候，子网格结束的时候
5. 共享内存和局部内存分别对于线程块和线程来说是私有的
6. 局部内存对线程私有，对外不可见。

# CUDA内存模型
GPU上的内存设备：

+ 寄存器：线程私有的存储，速度最快
    - 使用方式：声明私有变量或有常数长度的数组。
    - 注意：寄存器大小不够时会溢出到本地内存。
+ 本地内存：每个线程私有的本地内存
    - 使用方式：
        * 使用未知索引引用的本地数组
        * 可能会占用大量寄存器空间的较大本地数组或者结构体
        * 任何不满足核函数寄存器限定条件的变量
    - 硬件位置：SM的一级缓存，或者设备的二级缓存上。
+ 共享内存：每个线程块有自己的共享内存，对线程块内所有线程可见。可以被编程
    - 使用方式：`__share__`修饰
    - 同步：当需要通过共享数据来通信，可以使用同步语句：`void __syncthreads();`
    - 注意：不要因为过度使用共享内存，而导致SM上活跃的线程束减少；SM中的一级缓存，和共享内存共享一个片上内存，设置方式：`cudaError_t cudaFuncSetCacheConfig(const void * func, enum cudaFuncCache);`
+ 常量内存：驻留在设备内存中，所有线程都能访问，但是不能被核函数修改
    - 使用方式：`__constant__`修饰，主机端初始化后复制到设备端：`cudaError_t cudaMemcpyToSymbol(const void* symbol, const void *src, size_t count);`
    - 注意：当线程束中所有线程都从相同的地址取数据时，常量内存表现较好，因为一次读取会广播给所有线程束内的线程。如果不同的线程取不同地址的数据会效率下降。
+ 纹理内存：所有线程都能访问，但是不能写。对于某些特定的程序可能效果更好，比如需要滤波的程序，可以直接通过硬件完成。
+ 全局内存：GPU上最大的内存空间，延迟最高的内存
    - 使用方式：`__device__`修饰
    - 注意：全局内存访问是对齐，也就是一次要读取指定大小（32，64，128）整数倍字节的内存，所以当线程束执行内存加载/存储时，需要满足的传输数量通常取决于以下两个因素：
        * 跨线程的内存地址分布
        * 内存事务的对齐方式。

| **修饰符** | **变量名称** | **存储器** | **作用域** | **生命周期** |
| :---: | :---: | :---: | :---: | :---: |
|  | float var | 寄存器 | 线程 | 线程 |
|  | float var[100] | 本地 | 线程 | 线程 |
| __share__ | float var* | 共享 | 块 | 块 |
| __device__ | float var* | 全局 | 全局 | 应用程序 |
| __constant | float var* | 常量 | 全局 | 应用程序 |


## GPU缓存
GPU缓存不可编程，其行为出厂是时已经设定好了。GPU上有4种缓存：

1. 一级缓存
2. 二级缓存
3. 只读常量缓存
4. 只读纹理缓存

每个SM都有一个一级缓存，所有SM公用一个二级缓存。一级、二级缓存的作用都是被用来存储本地内存和全局内存中的数据，也包括寄存器溢出的部分。Fermi，Kepler以及以后的设备，CUDA允许我们配置读操作的数据是使用一级缓存和二级缓存，还是只使用二级缓存。

与CPU不同的是，CPU读写过程都有可能被缓存，但是GPU写的过程不被缓存，只有加载会被缓存！

每个SM有一个只读常量缓存，只读纹理缓存，它们用于设备内存中提高来自于各自内存空间内的读取性能。

| **存储器** | **片上/片外** | **缓存** | **存取** | **范围** | **生命周期** |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 寄存器 | 片上 | n/a | R/W | 一个线程 | 线程 |
| 本地 | 片外 | 1.0以上有 | R/W | 一个线程 | 线程 |
| 共享 | 片上 | n/a | R/W | 块内所有线程 | 块 |
| 全局 | 片外 | 1.0以上有 | R/W | 所有线程+主机 | 主机配置 |
| 常量 | 片外 | Yes | R | 所有线程+主机 | 主机配置 |
| 纹理 | 片外 | Yes | R | 所有线程+主机 | 主机配置 |


### 内存访问模式
类似C++，字节对齐、合并访问，最大化内存读取效率==最小化内存访问次数。写出Cache友好的代码==写出SM友好的代码。


```
struct A a[N];
```

```
struct A{
    int a[N];
    int b[N]
}a;
```


CUDA对细粒度数组是非常友好的，但是对粗粒度如结构体组成的数组就不太友好了，具体表现在，内存访问利用率低。比如当一个线程要访问结构体中的某个成员的时候，当三十二个线程同时访问的时候，SoA的访问就是连续的，而AoS则是不连续：  
<img src="https://intranetproxy.alipay.com/skylark/lark/0/2026/png/180556543/1768825525575-bda0a190-6f3c-4a7b-91de-df4bd6653b31.png" width="1644" title="" crop="0,0,1,1" id="ud3cb6ffe" class="ne-image">  
这样看来AoS访问效率只有 50%  
对比AoS和SoA的内存布局，我们能得到下面结论。

+ 并行编程范式，尤其是SIMD（单指令多数据）对SoA更友好。CUDA中普遍倾向于SoA因为这种内存访问可以有效地合并。



优化设备内存带宽利用率有两个目标：

1. 对齐、合并内存访问，以减少带宽的浪费
2. 足够的并发内存操作，以隐藏内存延迟




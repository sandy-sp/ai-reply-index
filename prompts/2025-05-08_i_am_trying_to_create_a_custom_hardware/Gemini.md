# Response from Gemini

\*\*

# Direct Boot of Large Language Models on Custom Hardware: A Feasibility

Analysis

The query regarding the creation of custom hardware capable of directly
booting and running large language models (LLMs), bypassing the need for a
traditional operating system, presents an intriguing challenge at the
intersection of artificial intelligence and embedded systems. Such an
endeavor, while ambitious, holds the potential for significant advantages,
including enhanced performance by eliminating the overhead associated with an
operating system.1 Reduced latency, crucial for real-time applications
leveraging LLMs, could also be achieved.3 Furthermore, by running only the
necessary code, power consumption might be lowered, which is particularly
important for edge deployments.6 Finally, a minimized software stack could
lead to enhanced security by reducing the attack surface.4

However, realizing this vision entails navigating a complex landscape of
technical hurdles. These include the intricate development of a bootloader
capable of loading and executing a large and sophisticated model, the
necessity for manual memory management and resource allocation typically
handled by an OS, the absence of readily available operating system services
and abstractions, and the fundamental requirement of initializing the custom
hardware and managing its peripherals directly.

The user's concept of a specialized system, devoid of a general-purpose
operating system, allows for a high degree of tailoring of both hardware and
software specifically for the task of running the target LLM. This extreme
specialization offers a pathway to efficiency gains that might be unattainable
when running an LLM on general-purpose hardware managed by a conventional
operating system. The numerous services and drivers included in a typical OS,
while providing flexibility for a wide range of applications, inevitably
consume computational resources and memory, introducing overhead that a
direct-boot system could potentially avoid.

Conversely, this intense focus on a single task comes with an inherent trade-
off in flexibility. A system designed to boot directly into an LLM would be
tightly coupled to that specific model and its requirements. Any deviation,
whether a change in the LLM itself or a desire to utilize the hardware for
other computational tasks, would likely necessitate substantial re-engineering
of the system. An operating system, by its nature, provides an abstraction
layer that allows diverse applications to run on the same underlying hardware.
The absence of this layer in a direct-boot scenario means that the hardware
and the LLM are intrinsically linked.

2\. Understanding the Boot Process and Bare-Metal Execution

The standard boot sequence of a computer typically begins with the application
of power, which triggers the initialization of the system's firmware, commonly
known as BIOS or UEFI.8 This firmware performs a power-on self-test (POST) to
check the basic functionality of the hardware and initializes core components
such as the CPU and memory.11 Following this initial phase, the firmware
searches for and loads a bootloader from a designated boot device, such as a
hard drive or USB drive.11 The bootloader's primary role is then to load the
operating system kernel into the system's memory and transfer control of the
machine to the kernel.11 Finally, the OS kernel takes over, initializing
system services and eventually starting user-level applications.

In contrast to this OS-centric model, bare-metal programming involves the
direct execution of code on the hardware without the intermediary of an
operating system.8 This paradigm necessitates direct interaction with the
hardware's registers and peripherals, giving the programmer fine-grained
control over the system's behavior.16 Bare-metal environments typically
feature minimal or no abstraction layers, placing the responsibility for
resource management and hardware interaction directly on the application
developer.4 This approach is commonly employed in embedded systems, real-time
applications where precise timing is critical, and high-performance computing
scenarios where specific tasks demand maximum efficiency.4 In a bare-metal
system, the bootloader's role shifts to directly loading and executing the
target application, which in the user's case would be the LLM.8

Achieving the user's goal of booting directly into an LLM is indeed possible
through the creation of a custom bootloader.11 This specialized bootloader
would need to initialize the hardware components essential for the LLM's
operation and then directly load and start the LLM's pre-compiled executable
code.11 This requires the LLM to be compiled into a format that the bootloader
can directly load into memory and execute.11 Furthermore, the custom
bootloader would need to handle fundamental tasks that are typically the
domain of an operating system, such as setting up memory regions for the LLM's
code and data, and potentially managing basic hardware interfaces that the LLM
relies upon.

Even in a scenario where the intention is to bypass a full operating system,
the system's initial startup will invariably depend on the foundational
firmware present on the hardware, whether it is a traditional BIOS or the more
modern UEFI.8 Upon power-on, the CPU begins executing code from a designated
address within the firmware ROM. This initial firmware is responsible for the
most basic level of hardware initialization, such as setting up the CPU and
essential chipsets. Therefore, a completely OS-less boot process still
necessitates this initial firmware stage to perform the very first steps of
hardware enablement and to ultimately hand over control to the subsequent
stage, which in this case would be the custom bootloader designed to load the
LLM.

The feasibility of directly booting into an LLM is heavily contingent upon the
complexity and the capabilities of the custom bootloader that would need to be
developed.15 A standard bootloader is primarily designed to locate and load an
operating system, which then takes on the responsibility of managing
applications. In contrast, for a direct-boot LLM, the bootloader effectively
assumes the role of a highly minimal operating system, tasked with setting up
the specific runtime environment that the LLM requires to operate. This
necessitates a bootloader with capabilities far beyond those of a typical OS
loader.

3\. Hardware Requirements for Large Language Models

Running large language models efficiently demands significant hardware
resources. In terms of processing power, Graphics Processing Units (GPUs) have
become the cornerstone for LLM workloads due to their inherent parallel
processing capabilities, which align well with the matrix multiplications and
other computations at the heart of deep learning.6 While GPUs handle the bulk
of the model computations, a powerful Central Processing Unit (CPU) with a
high core count remains essential for managing data pipelines, preprocessing
tasks, and coordinating operations between different hardware components.41
Beyond CPUs and GPUs, the field is seeing increasing interest in specialized
AI accelerators like Tensor Processing Units (TPUs), Field-Programmable Gate
Arrays (FPGAs), and Application-Specific Integrated Circuits (ASICs), which
are being developed to further optimize LLM performance and energy
efficiency.44

Memory is another critical aspect. LLMs, with their billions of parameters,
require substantial Video Random Access Memory (VRAM) to store these
parameters for efficient inference and training.41 The specific amount of VRAM
needed is directly proportional to the size of the LLM, typically measured by
the number of its parameters.46 In addition to VRAM, ample system RAM is
necessary for handling the large datasets involved, for intermediate
computations during LLM execution, and potentially for storing portions of the
model if the VRAM capacity is a limitation.41 NVIDIA, a leading provider of
GPUs for AI, recommends that the system have at least twice the amount of CPU
system memory as the total GPU VRAM to accommodate efficient buffering.42

Fast storage solutions are also paramount for LLM workloads. High-speed NVMe
Solid State Drives (SSDs) are crucial for rapidly loading the LLM model and
the associated datasets into memory.41 The overall storage requirements depend
on the size of the specific LLM being used and any additional data it might
need to access.42 Finally, for systems employing multiple GPUs to handle very
large models, high-speed interconnects like NVLink become important to
facilitate efficient communication and memory sharing between the GPUs.41

The amount of available VRAM often acts as the primary bottleneck when working
with LLMs, effectively setting an upper limit on the size of the model that
can be handled without significant performance degradation.42 LLMs consist of
a vast number of parameters that the processing units need to access quickly
for computations. These parameters are typically stored in the high-bandwidth
GPU memory for this very reason. If the size of the LLM exceeds the VRAM
capacity of the installed GPUs, the system will be forced to move data between
the slower system RAM and the VRAM, leading to a substantial drop in
performance.

Ongoing research into custom hardware solutions like FPGAs and ASICs for
accelerating LLMs 6 is largely motivated by the need to overcome the
limitations of general-purpose GPUs, particularly in terms of energy
efficiency and potentially latency. These factors could be especially critical
for a direct-boot system designed to run a specific LLM. While GPUs offer
considerable parallel processing power, they are designed to be versatile and
might not be perfectly optimized for the specific computational patterns found
in all LLM architectures. Custom hardware allows for the creation of
architectures that are precisely tailored to the unique computational demands
of LLMs, potentially resulting in better performance per watt and lower
overall latency.

4\. Exploring Custom Hardware Solutions for LLM Acceleration

Field-Programmable Gate Arrays (FPGAs) represent a class of reconfigurable
hardware that can be customized to accelerate specific computational
workloads, including those associated with large language models.6 FPGAs offer
a significant degree of flexibility, allowing developers to design and
implement custom hardware architectures that can be optimized for low latency
and high energy efficiency.6 Research in this area has demonstrated the
potential for FPGAs to achieve substantial speedups and energy efficiency
improvements compared to traditional GPUs for certain LLM tasks.6 Notably,
researchers have reported achieving 50 times greater efficiency than GPUs by
running a billion-parameter LLM on custom hardware based on an FPGA, with a
power consumption of only 13 watts.6 This achievement involved eliminating the
computationally intensive matrix multiplication operations typically used in
neural networks and leveraging a custom hardware prototype built on an FPGA to
fully exploit energy-saving features programmed into their neural network. The
resulting system was able to process text at a rate faster than human reading
speed while operating on a remarkably low power budget.

Application-Specific Integrated Circuits (ASICs) take the concept of custom
hardware a step further by being designed and fabricated specifically for a
particular application or set of applications, offering the potential for
maximum performance and energy efficiency.44 ASICs can be highly optimized for
the specific computational demands of LLMs, allowing for significant gains in
speed and power consumption.47 A prominent example in the field of AI is
Google's Tensor Processing Unit (TPU), which was developed specifically to
accelerate deep learning workloads.44 Early research into the use of ASICs for
transformer networks, the underlying architecture of many modern LLMs, has
shown promising results, with significant speedups and energy efficiency
improvements compared to both CPUs and GPUs.47 For instance, the A3 ASIC
demonstrated up to a 7x speedup and an 11x improvement in energy efficiency
compared to an Intel Gold 6128 CPU for attention mechanism computations.47
Another ASIC, ELSA, achieved even more impressive results, showing up to a
157x speedup over GPUs for the self-attention computation within transformer
networks.47

Neuromorphic computing represents an alternative computing paradigm that draws
inspiration from the structure and function of the human brain.76 This
approach typically utilizes spiking neural networks and event-driven
processing, which hold the potential for ultra-low power consumption,
mimicking the energy efficiency of biological systems.76 Early research in
this area has indicated the promise of neuromorphic hardware for efficient LLM
inference.76 For example, researchers working with Intel's Loihi 2
neuromorphic processor presented a novel MatMul-free LLM architecture that, in
preliminary findings, demonstrated up to a 3x higher throughput and a 2x
reduction in energy consumption compared to transformer-based LLMs running on
an edge GPU.76 Despite these promising results, neuromorphic computing remains
largely in the research and development phase and has not yet seen widespread
adoption in practical applications.77

FPGAs offer a compelling middle ground between the versatility of software-
based solutions running on general-purpose processors and the ultimate
efficiency of custom-designed ASICs.6 They provide a means to implement custom
hardware architectures with a more manageable timeframe and lower initial
costs compared to the significant investment required for ASIC design and
fabrication. This makes FPGAs a potentially valuable platform for prototyping
and validating the concept of a direct-boot LLM system before committing to a
more specialized ASIC implementation.

A significant driving force behind the exploration of custom hardware,
particularly FPGAs and neuromorphic chips, for LLMs is the imperative to
address the substantial energy consumption associated with training and
operating these large models.6 The operational costs and environmental impact
of LLMs are considerable, making energy efficiency a critical concern. Custom
hardware solutions are being actively investigated as a way to dramatically
reduce the power requirements for running LLMs, which would be a significant
advantage for a dedicated, direct-boot LLM device, especially for deployments
at the edge where power resources might be constrained.

Accelerator Type| Key Characteristics| Pros| Cons| Examples\
---|---|---|---|---\
GPU| Parallel processing, high throughput| Widely available, mature software
ecosystem| Can be power-hungry, not always optimal for specific LLM
operations| NVIDIA RTX/A/H series, AMD Radeon Pro\
TPU| Custom ASIC optimized for deep learning (TensorFlow)| High performance
for TensorFlow workloads, energy efficient| Primarily for Google Cloud, less
general-purpose| Google TPUs\
FPGA| Reconfigurable hardware| Flexible, can be optimized for low latency and
energy efficiency| More complex programming than GPUs, lower peak performance|
Xilinx Alveo, Intel Arria/Stratix, Achronix Speedster\
ASIC| Custom-designed chip for specific applications| Maximum performance and
energy efficiency for targeted workloads| High development cost and time, less
flexible| Google TPUs, custom accelerators (A3, ELSA)\
Neuromorphic| Brain-inspired, spiking neural networks, event-driven| Potential
for ultra-low power consumption, biologically plausible| Still in research
phase, limited availability and software support| Intel Loihi, IBM TrueNorth,
Akida NSoC

5\. The Feasibility of a Direct-Boot LLM System

The linchpin of a direct-boot LLM system on custom hardware would be a highly
specialized bootloader. This bootloader would need to perform a minimal set of
hardware initializations, focusing only on the components that the LLM
requires to operate. For ARM Cortex processors, this includes essential steps
like configuring the clock system, initializing the memory controller and RAM,
and setting the vector table and stack pointers before transferring control to
the application.23 The bootloader's core function would then be to load the
pre-compiled LLM directly from a non-volatile storage medium, such as flash
memory or an external memory interface like QSPI, into the appropriate memory
locations.23 This process would necessitate a deep understanding of the
system's memory layout and the specific format in which the LLM has been
compiled.

Beyond loading, the bootloader might also need to set up specific memory
regions required by the LLM for its parameters, activations, and working
memory. It could also be responsible for initializing basic peripherals that
the LLM might need for input or output, such as configuring GPIO pins or
setting up communication interfaces like UART or Ethernet.23 Finally, the
bootloader would transfer the execution flow to the LLM's designated entry
point in memory.23 This often involves disabling any interrupts that were
active during the boot process and setting the program counter to the starting
address of the LLM's code.25

Designing such a bootloader involves several critical considerations. The
initial boot stage might have severe size constraints, as exemplified by the
Master Boot Record (MBR) on x86 systems, which is limited to 512 bytes.11 This
might necessitate a multi-stage bootloader approach, where a small initial
bootloader loads a more capable second-stage bootloader from storage.11 The
bootloader must also be designed to interface with the specific non-volatile
storage medium where the LLM is stored, which could be internal flash memory
or external devices.90 Furthermore, for a practical system, the bootloader
should ideally include mechanisms for updating the LLM firmware, allowing for
bug fixes, performance enhancements, or even the deployment of newer LLM
versions.23 Techniques like A/B partitioning, where two copies of the firmware
are stored, can improve the robustness of the update process.37 Finally,
security is a crucial aspect, and the bootloader should incorporate measures
to prevent unauthorized modifications to the LLM, such as cryptographic
signatures to verify the integrity of the firmware before loading and
execution.24

To run directly on bare metal, the LLM itself, typically developed using high-
level frameworks like PyTorch or TensorFlow, would need to be adapted or a
specific model chosen that can be compiled into a self-contained executable.41
This process might involve using specialized tools or libraries designed for
embedded machine learning, such as TinyML, or developing a custom compilation
flow to generate code that can run without the extensive runtime dependencies
of a full OS. Standard LLM frameworks rely heavily on OS-level functionalities
for tasks like memory management and file system access, so these dependencies
would need to be carefully addressed. Furthermore, meticulous planning of the
memory layout and addressing scheme within the bare-metal environment is
essential. Linker scripts would play a vital role in ensuring that different
sections of the LLM's code and data are placed in the correct memory regions
accessible by the bootloader and the LLM during execution.25

Even in the absence of a complete operating system, a minimal Hardware
Abstraction Layer (HAL) might prove necessary to provide a consistent
interface for the LLM to interact with the custom hardware.41 This HAL would
essentially be a set of custom-developed drivers for the various hardware
components present in the system. It could include routines for accessing
memory, controlling communication interfaces like UART or Ethernet, and
interacting with any other peripherals that the LLM requires for its
operation, such as sensors for input or actuators for output.

The custom bootloader in this scenario transcends the role of a mere OS
loader; it effectively becomes a highly specialized, minimal runtime
environment tailored to the specific needs of the LLM.23 It takes on
responsibilities that typically fall under the purview of an operating system,
such as hardware initialization, loading a complex application, setting up its
memory space, and potentially providing rudimentary services through a HAL.
This blurring of the lines between a traditional bootloader and a very basic,
single-application OS highlights the complexity involved in such a direct-boot
system.

A significant challenge lies in the compatibility of existing LLM frameworks
with a bare-metal environment.41 These frameworks are generally designed to
operate on top of an OS, which offers a rich set of abstractions and services
that simplify application development. Adapting an LLM, developed using such a
framework, to run directly on bare metal without these underlying OS
functionalities would likely require a substantial engineering effort. It
might not even be feasible for all frameworks or LLM model architectures.
Overcoming this hurdle might necessitate the use of specialized, lightweight
LLM inference libraries that are specifically designed for deployment in
resource-constrained embedded systems, or a significant re-architecting of the
LLM's dependencies.

6\. Memory Management and Resource Allocation in a Bare-Metal LLM

In a bare-metal LLM system, the absence of an operating system means there is
no built-in virtual memory, paging mechanisms, or dynamic memory allocation
typically provided by an OS.8 Consequently, memory management becomes the sole
responsibility of the bootloader and the LLM software itself.17 The memory
layout of the system, including the allocation of memory regions for the LLM's
code, its extensive parameter data, the runtime stack, and any necessary
buffers, must be meticulously defined and managed explicitly.17 This requires
a thorough understanding of the memory architecture of the custom hardware and
the specific memory usage patterns of the target LLM.

The most likely approach to memory management in such a system would involve
static allocation, where memory regions are pre-allocated either at compile
time or during the initialization phase of the bootloader.27 This method
simplifies memory management but necessitates knowing the precise memory
requirements of the LLM model in advance.46 This might involve a detailed
analysis of the LLM's architecture and its memory footprint based on the
number of parameters and the precision used to represent them.

Handling very large LLMs in a bare-metal environment presents significant
challenges, particularly when the custom hardware has limited memory
resources.42 In such cases, techniques like model parallelism, where the
model's computations are distributed across multiple processing units, or
offloading parts of the model to slower but larger memory might need to be
considered. A crucial optimization for running LLMs on resource-constrained
hardware is quantization, which involves reducing the precision of the model's
weights and activations, thereby significantly decreasing its memory
footprint.66 Unlike systems with operating systems that can attempt dynamic
memory allocation, bare-metal systems typically avoid this due to the
potential for memory fragmentation.94 Therefore, static allocation, while
requiring careful upfront planning, is generally the preferred and more stable
approach.

Finally, the bootloader might also need to handle the allocation of specific
hardware resources required for the LLM's execution. For instance, if the
custom hardware includes a dedicated AI accelerator like an FPGA or ASIC, the
bootloader would need to initialize and configure this accelerator, making its
processing cores and memory accessible to the LLM's execution flow.

In a bare-metal LLM system, the responsibility for managing the system's
memory rests entirely with the developer. Without the memory management and
protection mechanisms offered by an operating system, any errors in memory
allocation or management can lead to critical system failures or unpredictable
behavior.17 Therefore, a deep understanding of the hardware's memory
architecture and the LLM's specific memory needs is paramount. Careful
planning, potentially involving the creation of detailed memory maps defined
in linker scripts, along with the implementation of custom memory management
routines, will be essential to prevent memory corruption and ensure the
overall stability of the system.

Given the potentially immense memory requirements of LLMs, especially for
larger models with billions of parameters, the application of quantization
techniques will likely be a key enabler for making a direct-boot system
feasible on custom hardware with limited memory resources.66 By reducing the
number of bits used to represent the model's weights and activations,
quantization can significantly decrease the overall memory footprint of the
LLM. This reduction is crucial for allowing larger models to potentially fit
within the constraints of smaller memory capacities, which is often the case
in embedded or custom hardware designs compared to the more abundant resources
available in server-grade environments.

7\. Firmware Initialization and Hardware Enablement for a Custom LLM System

The journey to booting a custom AI hardware system directly into an LLM begins
with the crucial step of firmware initialization. The custom bootloader, or
potentially a very early stage firmware component, needs to perform the
initial setup of the essential hardware components.23 This includes bringing
up the CPU core(s) and configuring their basic registers to a known and
operational state. The memory controller must be initialized to enable access
to the system's RAM, and the clock system and power management units need to
be configured to ensure the correct operating frequencies and power modes for
optimal performance and efficiency.23 These low-level initialization tasks
often involve direct manipulation of hardware registers, requiring a thorough
understanding of the specific hardware architecture and its register map,
typically found in the device's technical documentation.16

If the custom hardware incorporates a dedicated AI accelerator, such as an
FPGA or an ASIC, the bootloader must also handle its initialization and
configuration.6 For FPGAs, this might involve loading a specific configuration
bitstream that defines the custom hardware architecture. In the case of ASICs,
it could entail loading specific firmware or configuration data required for
the accelerator to function correctly. For example, Habana Gaudi AI
accelerators necessitate the loading of specific firmware during the
initialization process.96

Furthermore, the bootloader needs to initialize any peripherals that the LLM
will rely upon for its operation.17 This could include setting up
communication interfaces like UART for serial communication with external
devices or network interfaces like Ethernet for network-based input or output.
The specific peripherals that need initialization will depend on the intended
application and how the LLM will interact with the outside world.

Developing the firmware and bootloader for such a custom system typically
involves the use of low-level programming languages like C or assembly.16
These languages provide the necessary level of control over the hardware to
perform the intricate initialization steps. The development process also
requires the use of specialized Integrated Development Environments (IDEs) and
toolchains that are specific to the target hardware platform.17 For instance,
Keil MDK-ARM is a popular IDE for developing firmware for ARM-based
microcontrollers.17

Developing the firmware and bootloader for a custom AI hardware system demands
a profound understanding of the underlying hardware architecture. This
includes not only the CPU and memory subsystems but also any specialized AI
accelerators that are part of the design.10 Without the abstraction provided
by an operating system, developers must have a detailed knowledge of how each
hardware component functions and how to configure it at a very low level. This
often involves in-depth study of hardware manuals and datasheets to understand
the register map and the sequence of operations required for proper
initialization. Tools such as hardware debuggers and emulators 17 become
indispensable for tracing the execution of the firmware and identifying and
resolving any initialization issues.

For the long-term viability of a direct-boot LLM system, the ability to
perform firmware updates is crucial.23 This includes the need to update the
LLM model itself to incorporate bug fixes, performance improvements, or even
entirely new model versions. The bootloader must be designed to include
mechanisms for receiving and installing these updates, which might involve
over-the-air (OTA) update capabilities if the hardware has network
connectivity 24, or the ability to update from an external storage medium.
Implementing robust update mechanisms, potentially including features like
dual boot partitions to allow for rollback in case of a failed update 37, and
secure boot to verify the integrity of the new firmware 24, will be essential
to ensure the system remains functional and up-to-date over its lifespan.

8\. Trade-offs, Challenges, and Considerations

Embarking on the development of a custom hardware system that boots directly
into an LLM without an operating system presents a unique set of trade-offs.
On the positive side, such a system offers the potential for superior
performance and lower latency compared to systems running a general-purpose
OS, as the bare-metal approach eliminates the overhead associated with
virtualization and background processes.1 Optimized resource utilization and
potentially lower power consumption can also be achieved by running only the
code strictly necessary for the LLM.6 Furthermore, the absence of a full OS
can lead to a reduced complexity and a smaller attack surface, enhancing the
system's security.4 Finally, developers gain greater control over both the
hardware and software, allowing for fine-grained optimizations tailored to the
specific LLM workload.4

However, these advantages come with significant challenges. The development
complexity is considerably higher compared to building applications on top of
an existing operating system, as developers are responsible for managing
everything from low-level hardware initialization to memory allocation.17 This
necessitates a steeper learning curve and requires expertise in both bare-
metal programming and the intricacies of the target hardware architecture,
skill sets that might not be readily available.17 The lack of operating system
services, such as file system access, networking stacks, and device drivers,
means that these functionalities would need to be implemented from scratch if
the LLM requires them 8, a time-consuming and complex undertaking.108
Debugging in a bare-metal environment can also be more challenging due to the
absence of OS-level debugging tools and error logs, potentially requiring
custom debugging setups.8 Furthermore, the software ecosystem and the
availability of pre-built libraries are significantly more limited compared to
OS-based development, potentially leading to lower code reusability.19
Portability of the LLM and the bootloader to different hardware platforms can
also be a major challenge, as bare-metal code is typically tightly coupled to
the specific hardware architecture.19 Finally, achieving scalability in terms
of managing resources and handling multiple concurrent tasks might be more
limited compared to OS-based systems that can dynamically allocate and manage
resources.8

Several important considerations need to be taken into account when evaluating
the feasibility of such a project. The specific LLM model that the user
intends to run is a primary factor, as its size and computational requirements
will dictate the necessary hardware resources.46 The intended use case and the
desired performance goals, such as acceptable latency, required throughput,
and power consumption limits, will also heavily influence the design
decisions.3 The availability of resources and expertise within the development
team for tackling the complexities of bare-metal programming and hardware
architecture is another critical factor.17 Finally, the potential need for
future updates and modifications to the LLM model necessitates careful
planning for a robust update mechanism on the bare-metal system.23

Creating a custom direct-boot LLM system represents a substantial engineering
undertaking that demands specialized skills and a significant commitment of
time and resources.17 Unlike developing applications within the familiar
environment of an operating system, this approach requires building much of
the foundational software infrastructure from the ground up, including the
bootloader, potentially a minimal HAL, and ensuring the chosen LLM can be
adapted to run within this constrained environment. This necessitates a deep
and comprehensive understanding of both the target hardware and the principles
of low-level software development.

While the potential performance advantages of a direct-boot system are
compelling, particularly in scenarios where even small amounts of latency or
OS-induced overhead are unacceptable, these benefits must be carefully weighed
against the considerably increased complexity and overall effort associated
with the development and ongoing maintenance of such a system compared to
utilizing a standard operating system.1 For highly specific and performance-
critical applications, the gains in efficiency and control might indeed
justify the increased development burden. However, for more general use cases
or in situations where rapid development cycles and inherent flexibility are
important considerations, leveraging the well-established abstractions and
services provided by a standard operating system might ultimately prove to be
a more practical and cost-effective strategy.

9\. Conclusion and Future Directions

In conclusion, the creation of custom hardware that boots directly into
running a large language model without an operating system is technically
feasible, particularly with the advancements in custom hardware solutions like
FPGAs, as demonstrated by research achieving highly efficient LLM execution on
such platforms.6 However, realizing this concept presents significant
engineering challenges that necessitate expertise in bare-metal programming,
hardware architecture, and a deep understanding of the target LLM's
requirements.

The potential benefits of such a system, including enhanced performance,
improved energy efficiency, and a reduced security footprint, are compelling.
Nevertheless, the hurdles to overcome are substantial, primarily involving the
complex development of a specialized bootloader and firmware, the intricate
management of memory and hardware resources in the absence of an OS, and the
need to address the lack of readily available OS services and software
ecosystems.

Looking towards the future, several trends could make this endeavor more
accessible. Continued research into specialized hardware architectures
optimized for LLM inference, as highlighted in surveys of hardware
accelerators 47, is likely to yield more energy-efficient and performant
solutions. The development of lightweight LLM frameworks or model formats
specifically designed for bare-metal deployment could also lower the barrier
to entry. Furthermore, advancements in bootloader technology might lead to
more sophisticated solutions capable of handling the loading and
initialization of complex applications like LLMs with greater ease.

Ultimately, while the user's query represents an ambitious undertaking, it
also points to a potentially fruitful direction for exploring the boundaries
of LLM deployment, especially in the realm of highly specialized edge AI
applications where performance, efficiency, and control are of paramount
importance.

#### Works cited

1. Bare Metal vs. Traditional VMs for AI Fine-Tuning: What Should You Use? - RunPod, accessed May 8, 2025, [https://www.runpod.io/articles/comparison/bare-metal-vs-traditional-vms-ai-fine-tuning](https://www.runpod.io/articles/comparison/bare-metal-vs-traditional-vms-ai-fine-tuning)

1. Bare Metal vs. Traditional VMs: Which is Better for LLM Training? - RunPod, accessed May 8, 2025, [https://www.runpod.io/articles/comparison/bare-metal-vs-traditional-vms-llm-training](https://www.runpod.io/articles/comparison/bare-metal-vs-traditional-vms-llm-training)

1. OS-Level Challenges in LLM Inference and Optimizations - eunomia, accessed May 8, 2025, [https://eunomia.dev/blog/2025/02/18/os-level-challenges-in-llm-inference-and-optimizations/](https://eunomia.dev/blog/2025/02/18/os-level-challenges-in-llm-inference-and-optimizations/)

1. What are Bare Metal GPUs? | DigitalOcean, accessed May 8, 2025, [https://www.digitalocean.com/resources/articles/bare-metal-gpus](https://www.digitalocean.com/resources/articles/bare-metal-gpus)

1. How to Choose Between Bare Metal GPUs and Virtual GPUs for AI Workloads - Gcore, accessed May 8, 2025, [https://gcore.com/learning/bare-metal-vs-virtual-gpus](https://gcore.com/learning/bare-metal-vs-virtual-gpus)

1. Researchers run high-performing large language model on the ..., accessed May 8, 2025, [https://news.ucsc.edu/2024/06/matmul-free-llm/](https://news.ucsc.edu/2024/06/matmul-free-llm/)

1. Bare Metal vs. RTOS vs. OS: What Works Best for IoT? - Nabto, accessed May 8, 2025, [https://www.nabto.com/bare-metal-vs-rtos-vs-os/](https://www.nabto.com/bare-metal-vs-rtos-vs-os/)

1. What is Bare Metal Programming? The Basics Explained | Liquid Web, accessed May 8, 2025, [https://www.liquidweb.com/dedicated-server/what-is-bare-metal-programming/](https://www.liquidweb.com/dedicated-server/what-is-bare-metal-programming/)

1. Bare Metal Servers for AI and Machine Learning: The Ultimate Performance, accessed May 8, 2025, [https://www.bare-server.com/blog/bare-metal-servers-for-ai-and-machine-learning](https://www.bare-server.com/blog/bare-metal-servers-for-ai-and-machine-learning)

1. A Journey Through the Secrets of Firmware: From BIOS/UEFI to OS | HackerNoon, accessed May 8, 2025, [https://hackernoon.com/a-journey-through-the-secrets-of-firmware-from-biosuefi-to-os](https://hackernoon.com/a-journey-through-the-secrets-of-firmware-from-biosuefi-to-os)

1. How do operating systems… run… without having an OS to run in? - Software Engineering Stack Exchange, accessed May 8, 2025, [https://softwareengineering.stackexchange.com/questions/171127/how-do-operating-systems-run-without-having-an-os-to-run-in](https://softwareengineering.stackexchange.com/questions/171127/how-do-operating-systems-run-without-having-an-os-to-run-in)

1. What happens if I start PC without OS? : r/buildapc - Reddit, accessed May 8, 2025, [https://www.reddit.com/r/buildapc/comments/186mng7/what_happens_if_i_start_pc_without_os/](https://www.reddit.com/r/buildapc/comments/186mng7/what_happens_if_i_start_pc_without_os/)

1. How to run a program without an operating system? - Stack Overflow, accessed May 8, 2025, [https://stackoverflow.com/questions/22054578/how-to-run-a-program-without-an-operating-system](https://stackoverflow.com/questions/22054578/how-to-run-a-program-without-an-operating-system)

1. How to run a simple boot loader on real Hardware? : r/osdev - Reddit, accessed May 8, 2025, [https://www.reddit.com/r/osdev/comments/1i22f0g/how_to_run_a_simple_boot_loader_on_real_hardware/](https://www.reddit.com/r/osdev/comments/1i22f0g/how_to_run_a_simple_boot_loader_on_real_hardware/)

1. Writing a Custom Bootloader | Red Team Notes, accessed May 8, 2025, [https://www.ired.team/miscellaneous-reversing-forensics/windows-kernel-internals/writing-a-custom-bootloader](https://www.ired.team/miscellaneous-reversing-forensics/windows-kernel-internals/writing-a-custom-bootloader)

1. What is bare metal programming and how to get started? : r/embedded - Reddit, accessed May 8, 2025, [https://www.reddit.com/r/embedded/comments/10o0udj/what_is_bare_metal_programming_and_how_to_get/](https://www.reddit.com/r/embedded/comments/10o0udj/what_is_bare_metal_programming_and_how_to_get/)

1. Bare-Metal Programming: Optimizing Performance and Control - RunTime Recruitment, accessed May 8, 2025, [https://runtimerec.com/bare-metal-programming/](https://runtimerec.com/bare-metal-programming/)

1. What is RTOS vs. Bare Metal Programming: Which is Right for Your Embedded System?, accessed May 8, 2025, [https://www.hashstudioz.com/blog/what-is-rtos-vs-bare-metal-programming-which-is-right-for-your-embedded-system/](https://www.hashstudioz.com/blog/what-is-rtos-vs-bare-metal-programming-which-is-right-for-your-embedded-system/)

1. What is Bare Metal Programming in Embedded System? - InTechHouse, accessed May 8, 2025, [https://intechhouse.com/blog/what-is-bare-metal-programming-in-embedded-system/](https://intechhouse.com/blog/what-is-bare-metal-programming-in-embedded-system/)

1. RTOS vs. Bare Metal: Navigating Performance, Complexity, and Efficiency, accessed May 8, 2025, [https://weston-embedded.com/support/media-articles/119-rtos-vs-bare-metal-navigating-performance-complexity-and-efficiency](https://weston-embedded.com/support/media-articles/119-rtos-vs-bare-metal-navigating-performance-complexity-and-efficiency)

1. Bare Metal firmware development | Witekio, accessed May 8, 2025, [https://witekio.com/embedded-software/firmware/bare-metal-firmware-development/](https://witekio.com/embedded-software/firmware/bare-metal-firmware-development/)

1. hello world without an operating system - YouTube, accessed May 8, 2025, [https://www.youtube.com/watch?v=bpa5H6tnYZA](https://www.youtube.com/watch?v=bpa5H6tnYZA)

1. How to Create Bootloaders for Embedded Systems – Omi AI, accessed May 8, 2025, [https://www.omi.me/blogs/hardware-guides/how-to-create-bootloaders-for-embedded-systems](https://www.omi.me/blogs/hardware-guides/how-to-create-bootloaders-for-embedded-systems)

1. Understanding How Bootloaders Work - Parlez-vous Tech, accessed May 8, 2025, [https://www.parlezvoustech.com/en/comprendre-les-bootloaders/](https://www.parlezvoustech.com/en/comprendre-les-bootloaders/)

1. Creating a Custom Bootloader for a Cortex-M Microcontroller | DMC, Inc., accessed May 8, 2025, [https://www.dmcinfo.com/latest-thinking/blog/id/13707/creating-a-custom-bootloader-for-a-cortex-m-microcontroller](https://www.dmcinfo.com/latest-thinking/blog/id/13707/creating-a-custom-bootloader-for-a-cortex-m-microcontroller)

1. ARM: How to Write a Bootloader - Arm Developer, accessed May 8, 2025, [https://developer.arm.com/documentation/ka002218/latest/](https://developer.arm.com/documentation/ka002218/latest/)

1. Developing a simple bootloader for an Embedded system - Stack Overflow, accessed May 8, 2025, [https://stackoverflow.com/questions/24526760/developing-a-simple-bootloader-for-an-embedded-system](https://stackoverflow.com/questions/24526760/developing-a-simple-bootloader-for-an-embedded-system)

1. Custom bootloader best practice ? : r/embedded - Reddit, accessed May 8, 2025, [https://www.reddit.com/r/embedded/comments/d45816/custom_bootloader_best_practice/](https://www.reddit.com/r/embedded/comments/d45816/custom_bootloader_best_practice/)

1. Solved: Custom Bootloader? - STMicroelectronics Community, accessed May 8, 2025, [https://community.st.com/t5/stm32-mcus-embedded-software/custom-bootloader/td-p/76934](https://community.st.com/t5/stm32-mcus-embedded-software/custom-bootloader/td-p/76934)

1. Writing bootloaders for microcontrollers : r/embedded - Reddit, accessed May 8, 2025, [https://www.reddit.com/r/embedded/comments/n3caxu/writing_bootloaders_for_microcontrollers/](https://www.reddit.com/r/embedded/comments/n3caxu/writing_bootloaders_for_microcontrollers/)

1. What is a Bootloader and when do you need one? - EmbeddedRelated.com, accessed May 8, 2025, [https://www.embeddedrelated.com/thread/4393/what-is-a-bootloader-and-when-do-you-need-one](https://www.embeddedrelated.com/thread/4393/what-is-a-bootloader-and-when-do-you-need-one)

1. Bootloader Design for Microcontrollers in Embedded Systems, accessed May 8, 2025, [https://www.beningo.com/wp-content/uploads/images/Papers/bootloader_design_for_microcontrollers_in_embedded_systems%20.pdf](https://www.beningo.com/wp-content/uploads/images/Papers/bootloader_design_for_microcontrollers_in_embedded_systems%20.pdf)

1. Custom Boot-loader jump to application - C2000 microcontrollers forum - TI E2E, accessed May 8, 2025, [https://e2e.ti.com/support/microcontrollers/c2000-microcontrollers-group/c2000/f/c2000-microcontrollers-forum/113899/custom-boot-loader-jump-to-application](https://e2e.ti.com/support/microcontrollers/c2000-microcontrollers-group/c2000/f/c2000-microcontrollers-forum/113899/custom-boot-loader-jump-to-application)

1. From Zero to main(): How to Write a Bootloader from Scratch | Interrupt - Memfault, accessed May 8, 2025, [https://interrupt.memfault.com/blog/how-to-write-a-bootloader-from-scratch](https://interrupt.memfault.com/blog/how-to-write-a-bootloader-from-scratch)

1. Custom bootloader on the STM32L4 - STMicroelectronics Community, accessed May 8, 2025, [https://community.st.com/t5/stm32-mcus-products/custom-bootloader-on-the-stm32l4/td-p/50996](https://community.st.com/t5/stm32-mcus-products/custom-bootloader-on-the-stm32l4/td-p/50996)

1. TMS570LS0432: Custom Bootloader to Application Firmware - Arm-based microcontrollers forum - TI E2E - Texas Instruments, accessed May 8, 2025, [https://e2e.ti.com/support/microcontrollers/arm-based-microcontrollers-group/arm-based-microcontrollers/f/arm-based-microcontrollers-forum/590226/tms570ls0432-custom-bootloader-to-application-firmware](https://e2e.ti.com/support/microcontrollers/arm-based-microcontrollers-group/arm-based-microcontrollers/f/arm-based-microcontrollers-forum/590226/tms570ls0432-custom-bootloader-to-application-firmware)

1. Custom STM32 bootloader guidance - EEVblog, accessed May 8, 2025, [https://www.eevblog.com/forum/microcontrollers/custom-stm32-bootloader-guidance/](https://www.eevblog.com/forum/microcontrollers/custom-stm32-bootloader-guidance/)

1. Custom bootloader!!! (read comment) : r/osdev - Reddit, accessed May 8, 2025, [https://www.reddit.com/r/osdev/comments/1g0b8hq/custom_bootloader_read_comment/](https://www.reddit.com/r/osdev/comments/1g0b8hq/custom_bootloader_read_comment/)

1. Designing a Custom STM32 Bootloader: Practical Implementation - EmbeTronicX, accessed May 8, 2025, [https://embetronicx.com/tutorials/microcontrollers/stm32/bootloader/bootloader-in-stm32-bootloader-design/](https://embetronicx.com/tutorials/microcontrollers/stm32/bootloader/bootloader-in-stm32-bootloader-design/)

1. STM32 Tutorial #40 - Creating Custom Bootloader (USB DFU) and Relocated Application, accessed May 8, 2025, [https://www.youtube.com/watch?v=wirNEpE6Dd4](https://www.youtube.com/watch?v=wirNEpE6Dd4)

1. Best Hardware for Running Large Language Models LLMs, accessed May 8, 2025, [https://rational.co.in/best-hardware-for-running-large-language-models-llm/](https://rational.co.in/best-hardware-for-running-large-language-models-llm/)

1. Hardware Recommendations for Large Language Model Servers - Puget Systems, accessed May 8, 2025, [https://www.pugetsystems.com/solutions/ai-and-hpc-workstations/ai-large-language-models/hardware-recommendations/](https://www.pugetsystems.com/solutions/ai-and-hpc-workstations/ai-large-language-models/hardware-recommendations/)

1. Recommended Hardware for Running LLMs Locally | GeeksforGeeks, accessed May 8, 2025, [https://www.geeksforgeeks.org/recommended-hardware-for-running-llms-locally/](https://www.geeksforgeeks.org/recommended-hardware-for-running-llms-locally/)

1. Primer on Large Language Model (LLM) Inference Optimizations: 2. Introduction to Artificial Intelligence (AI) Accelerators | HackerNoon, accessed May 8, 2025, [https://hackernoon.com/primer-on-large-language-model-llm-inference-optimizations-2-introduction-to-artificial-intelligence-ai-accelerators](https://hackernoon.com/primer-on-large-language-model-llm-inference-optimizations-2-introduction-to-artificial-intelligence-ai-accelerators)

1. What are the Hardware Requirements for Large Language Model (LLM) Training?, accessed May 8, 2025, [https://www.appypieagents.ai/blog/hardware-requirements-for-llm-training](https://www.appypieagents.ai/blog/hardware-requirements-for-llm-training)

1. How Much Memory Needed for LLM | dasarpAI, accessed May 8, 2025, [https://dasarpai.com/dsblog/how-much-memory-needed-for-llm](https://dasarpai.com/dsblog/how-much-memory-needed-for-llm)

1. A Survey on Hardware Accelerators for Large Language Models - arXiv, accessed May 8, 2025, [https://arxiv.org/html/2401.09890v1](https://arxiv.org/html/2401.09890v1)

1. AI Accelerator | Fastly Products, accessed May 8, 2025, [https://docs.fastly.com/products/ai-accelerator](https://docs.fastly.com/products/ai-accelerator)

1. Benchmark Intel® Gaudi® 2 AI Accelerator for Large Language Models, accessed May 8, 2025, [https://www.intel.com/content/www/us/en/developer/articles/training/ai-accelerator-for-large-language-models.html](https://www.intel.com/content/www/us/en/developer/articles/training/ai-accelerator-for-large-language-models.html)

1. Generative AI Accelerator: The Efficient Hailo-10H M.2 Module, accessed May 8, 2025, [https://hailo.ai/products/ai-accelerators/hailo-10h-m-2-generative-ai-acceleration-module/](https://hailo.ai/products/ai-accelerators/hailo-10h-m-2-generative-ai-acceleration-module/)

1. arxiv.org, accessed May 8, 2025, [https://arxiv.org/pdf/2401.09890](https://arxiv.org/pdf/2401.09890)

1. [2401.09890] A Survey on Hardware Accelerators for Large Language Models - arXiv, accessed May 8, 2025, [https://arxiv.org/abs/2401.09890](https://arxiv.org/abs/2401.09890)

1. A Survey on Hardware Accelerators for Large Language Models - MDPI, accessed May 8, 2025, [https://www.mdpi.com/2076-3417/15/2/586](https://www.mdpi.com/2076-3417/15/2/586)

1. A Survey on Hardware Accelerators for Large Language Models - ResearchGate, accessed May 8, 2025, [https://www.researchgate.net/publication/390620220_A_Survey_on_Hardware_Accelerators_for_Large_Language_Models](https://www.researchgate.net/publication/390620220_A_Survey_on_Hardware_Accelerators_for_Large_Language_Models)

1. A Survey on Large Language Model Acceleration based on KV Cache Management - arXiv, accessed May 8, 2025, [https://arxiv.org/pdf/2412.19442?](https://arxiv.org/pdf/2412.19442)

1. Hardware Acceleration of LLMs: A comprehensive survey and comparison - arXiv, accessed May 8, 2025, [https://arxiv.org/abs/2409.03384](https://arxiv.org/abs/2409.03384)

1. Hardware Acceleration of LLMs: A comprehensive survey and comparison - arXiv, accessed May 8, 2025, [https://arxiv.org/html/2409.03384v1](https://arxiv.org/html/2409.03384v1)

1. Understanding the Potential of FPGA-Based Spatial Acceleration for Large Language Model Inference - arXiv, accessed May 8, 2025, [https://arxiv.org/html/2312.15159](https://arxiv.org/html/2312.15159)

1. FlightLLM: Efficient Large Language Model Inference with a Complete Mapping Flow on FPGAs, accessed May 8, 2025, [https://dai.sjtu.edu.cn/my_file/pdf/94c37d8a-7f86-4f95-ae72-05a79da5bb61.pdf](https://dai.sjtu.edu.cn/my_file/pdf/94c37d8a-7f86-4f95-ae72-05a79da5bb61.pdf)

1. kachris/survey_HA_LLM: A survey on Hardware Accelerated LLMs - GitHub, accessed May 8, 2025, [https://github.com/kachris/survey_HA_LLM](https://github.com/kachris/survey_HA_LLM)

1. Understanding the Potential of FPGA-Based Spatial Acceleration for Large Language Model Inference | Request PDF - ResearchGate, accessed May 8, 2025, [https://www.researchgate.net/publication/379584970_Understanding_the_Potential_of_FPGA-Based_Spatial_Acceleration_for_Large_Language_Model_Inference](https://www.researchgate.net/publication/379584970_Understanding_the_Potential_of_FPGA-Based_Spatial_Acceleration_for_Large_Language_Model_Inference)

1. FPGA-Accelerated Large Language Models Used for ChatGPT, accessed May 8, 2025, [https://www.achronix.com/blog/fpga-accelerated-large-language-models-used-chatgpt](https://www.achronix.com/blog/fpga-accelerated-large-language-models-used-chatgpt)

1. Accelerating LLM Inferencing on FPGAs | Achronix Semiconductor Corporation, accessed May 8, 2025, [https://www.achronix.com/blog/accelerating-llm-inferencing-fpgas](https://www.achronix.com/blog/accelerating-llm-inferencing-fpgas)

1. [2312.15159] Understanding the Potential of FPGA-Based Spatial Acceleration for Large Language Model Inference - arXiv, accessed May 8, 2025, [https://arxiv.org/abs/2312.15159](https://arxiv.org/abs/2312.15159)

1. The Rise of FPGA-Accelerated LLMs - YouTube, accessed May 8, 2025, [https://www.youtube.com/watch?v=hoIMDKrT6jM](https://www.youtube.com/watch?v=hoIMDKrT6jM)

1. Hardware requirements for running the large language model Deepseek R1 locally., accessed May 8, 2025, [https://www.rnfinity.com/news-show/Hardware-requirements-for-running-large-language-model-Deepseek-R1-on-a-local-machine](https://www.rnfinity.com/news-show/Hardware-requirements-for-running-large-language-model-Deepseek-R1-on-a-local-machine)

1. What Hardware Do You Need for Running LLMs on the Desktop? - Redmondmag.com, accessed May 8, 2025, [https://redmondmag.com/articles/2025/04/16/what-hardware-do-you-need-for-running-llms-on-the-desktop.aspx](https://redmondmag.com/articles/2025/04/16/what-hardware-do-you-need-for-running-llms-on-the-desktop.aspx)

1. PSA: Local LLM Hardware Requirements : r/homeassistant - Reddit, accessed May 8, 2025, [https://www.reddit.com/r/homeassistant/comments/1hovutx/psa_local_llm_hardware_requirements/](https://www.reddit.com/r/homeassistant/comments/1hovutx/psa_local_llm_hardware_requirements/)

1. How to Run an LLM Locally with Pieces, accessed May 8, 2025, [https://pieces.app/blog/how-to-run-an-llm-locally-with-pieces](https://pieces.app/blog/how-to-run-an-llm-locally-with-pieces)

1. LLM Training & GPU Memory Requirements: Examples - Analytics Yogi, accessed May 8, 2025, [https://vitalflux.com/llm-gpu-memory-requirements-examples/](https://vitalflux.com/llm-gpu-memory-requirements-examples/)

1. The Complete Guide to GPU Requirements for LLM Fine-tuning - RunPod Blog, accessed May 8, 2025, [https://blog.runpod.io/the-complete-guide-to-gpu-requirements-for-llm-fine-tuning/](https://blog.runpod.io/the-complete-guide-to-gpu-requirements-for-llm-fine-tuning/)

1. Optimizing LLMs for Speed and Memory - Hugging Face, accessed May 8, 2025, [https://huggingface.co/docs/transformers/v4.35.0/llm_tutorial_optimization](https://huggingface.co/docs/transformers/v4.35.0/llm_tutorial_optimization)

1. Understanding Large Language Model Parameters and Memory Requirements: A Deep Dive - Unite.AI, accessed May 8, 2025, [https://www.unite.ai/understanding-large-language-model-parameters-and-memory-requirements-a-deep-dive/](https://www.unite.ai/understanding-large-language-model-parameters-and-memory-requirements-a-deep-dive/)

1. [2406.08413] Memory Is All You Need: An Overview of Compute-in-Memory Architectures for Accelerating Large Language Model Inference - arXiv, accessed May 8, 2025, [https://arxiv.org/abs/2406.08413](https://arxiv.org/abs/2406.08413)

1. How to estimate memory requirements for LLM pre-training? - Reddit, accessed May 8, 2025, [https://www.reddit.com/r/learnmachinelearning/comments/1hwoiyr/how_to_estimate_memory_requirements_for_llm/](https://www.reddit.com/r/learnmachinelearning/comments/1hwoiyr/how_to_estimate_memory_requirements_for_llm/)

1. Neuromorphic Principles for Efficient Large Language Models on Intel Loihi 2 - arXiv, accessed May 8, 2025, [https://arxiv.org/abs/2503.18002](https://arxiv.org/abs/2503.18002)

1. Neuromorphic computing: the future of AI | LANL, accessed May 8, 2025, [https://www.lanl.gov/media/publications/1663/1269-neuromorphic-computing](https://www.lanl.gov/media/publications/1663/1269-neuromorphic-computing)

1. [2501.16337] Explore Activation Sparsity in Recurrent LLMs for Energy-Efficient Neuromorphic Computing - arXiv, accessed May 8, 2025, [https://arxiv.org/abs/2501.16337](https://arxiv.org/abs/2501.16337)

1. Neuromorphic computing and AI : r/skeptic - Reddit, accessed May 8, 2025, [https://www.reddit.com/r/skeptic/comments/1joftf9/neuromorphic_computing_and_ai/](https://www.reddit.com/r/skeptic/comments/1joftf9/neuromorphic_computing_and_ai/)

1. On Unconventional Computing for LLMs : r/LocalLLaMA - Reddit, accessed May 8, 2025, [https://www.reddit.com/r/LocalLLaMA/comments/1bpva3a/on_unconventional_computing_for_llms/](https://www.reddit.com/r/LocalLLaMA/comments/1bpva3a/on_unconventional_computing_for_llms/)

1. Neuromorphic Computing The Next Frontier in Brain-Inspired AI, Scalable Architectures, and Intelligent Systems - ResearchGate, accessed May 8, 2025, [https://www.researchgate.net/publication/388876273_Neuromorphic_Computing_The_Next_Frontier_in_Brain-Inspired_AI_Scalable_Architectures_and_Intelligent_Systems](https://www.researchgate.net/publication/388876273_Neuromorphic_Computing_The_Next_Frontier_in_Brain-Inspired_AI_Scalable_Architectures_and_Intelligent_Systems)

1. Neuromorphic computing - Wikipedia, accessed May 8, 2025, [https://en.wikipedia.org/wiki/Neuromorphic_computing](https://en.wikipedia.org/wiki/Neuromorphic_computing)

1. What Is Neuromorphic Computing? - IBM, accessed May 8, 2025, [https://www.ibm.com/think/topics/neuromorphic-computing](https://www.ibm.com/think/topics/neuromorphic-computing)

1. Neuromorphic Computing: Advancing Brain-Inspired Architectures for Efficient AI and Cognitive Applications - ScaleUp Lab Program, accessed May 8, 2025, [https://scaleuplab.gatech.edu/neuromorphic-computing-advancing-brain-inspired-architectures-for-efficient-ai-and-cognitive-applications/](https://scaleuplab.gatech.edu/neuromorphic-computing-advancing-brain-inspired-architectures-for-efficient-ai-and-cognitive-applications/)

1. Neuromorphic Computing and Hyper-Realistic Generative AI - The Digital Speaker, accessed May 8, 2025, [https://www.thedigitalspeaker.com/neuromorphic-computing-hyper-realistic-generative-ai/](https://www.thedigitalspeaker.com/neuromorphic-computing-hyper-realistic-generative-ai/)

1. Scaling up Neuromorphic Computing for More Efficient and Effective AI Everywhere and Anytime, accessed May 8, 2025, [https://today.ucsd.edu/story/scaling-up-neuromorphic-computing-for-more-efficient-and-effective-ai-everywhere-and-anytime](https://today.ucsd.edu/story/scaling-up-neuromorphic-computing-for-more-efficient-and-effective-ai-everywhere-and-anytime)

1. Neuromorphic artificial intelligence systems - Frontiers, accessed May 8, 2025, [https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2022.959626/full](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2022.959626/full)

1. A Survey on Neuromorphic Architectures for Running Artificial Intelligence Algorithms, accessed May 8, 2025, [https://www.mdpi.com/2079-9292/13/15/2963](https://www.mdpi.com/2079-9292/13/15/2963)

1. Integration of Hardware and Firmware in Embedded Systems - Arshon Inc. Blog, accessed May 8, 2025, [https://arshon.com/blog/integration-of-hardware-and-firmware-in-embedded-systems/](https://arshon.com/blog/integration-of-hardware-and-firmware-in-embedded-systems/)

1. Creating a custom bootloader and firmware in the same sector of the embedded flash memoery - STMicroelectronics Community, accessed May 8, 2025, [https://community.st.com/t5/stm32-mcus-products/creating-a-custom-bootloader-and-firmware-in-the-same-sector-of/td-p/630734](https://community.st.com/t5/stm32-mcus-products/creating-a-custom-bootloader-and-firmware-in-the-same-sector-of/td-p/630734)

1. How is BareMetalOS allocating memory in Assembly without malloc, brk, or mmap?, accessed May 8, 2025, [https://stackoverflow.com/questions/27727433/how-is-baremetalos-allocating-memory-in-assembly-without-malloc-brk-or-mmap](https://stackoverflow.com/questions/27727433/how-is-baremetalos-allocating-memory-in-assembly-without-malloc-brk-or-mmap)

1. Memory management in bare metal mode - AMD Adaptive Support, accessed May 8, 2025, [https://adaptivesupport.amd.com/s/question/0D52E00006hpUlKSAU/memory-management-in-bare-metal-mode?language=en_US](https://adaptivesupport.amd.com/s/question/0D52E00006hpUlKSAU/memory-management-in-bare-metal-mode?language=en_US)

1. Type-based memory safety without manual memory manage or runtime garbage collection?, accessed May 8, 2025, [https://cstheory.stackexchange.com/questions/39998/type-based-memory-safety-without-manual-memory-manage-or-runtime-garbage-collect](https://cstheory.stackexchange.com/questions/39998/type-based-memory-safety-without-manual-memory-manage-or-runtime-garbage-collect)

1. Bare-metal C++ object creation (and deletion) : r/embedded - Reddit, accessed May 8, 2025, [https://www.reddit.com/r/embedded/comments/tbvei6/baremetal_c_object_creation_and_deletion/](https://www.reddit.com/r/embedded/comments/tbvei6/baremetal_c_object_creation_and_deletion/)

1. Firmware Enablement: What, When, and How - rinf.tech, accessed May 8, 2025, [https://www.rinf.tech/firmware-enablement-what-when-and-how/](https://www.rinf.tech/firmware-enablement-what-when-and-how/)

1. Firmware Upgrade — Gaudi Documentation 1.20.1 documentation - Habana Labs, accessed May 8, 2025, [https://docs.habana.ai/en/latest/Installation_Guide/Firmware_Upgrade.html](https://docs.habana.ai/en/latest/Installation_Guide/Firmware_Upgrade.html)

1. Step-by-Step Guide to Developing Custom Firmware for IoT Devices - Omi, accessed May 8, 2025, [https://www.omi.me/blogs/hardware-guides/step-by-step-guide-to-developing-custom-firmware-for-iot-devices](https://www.omi.me/blogs/hardware-guides/step-by-step-guide-to-developing-custom-firmware-for-iot-devices)

1. Bare Metal Firmware Development: What, When and How - rinf.tech, accessed May 8, 2025, [https://www.rinf.tech/bare-metal-firmware-development-what-when-and-how/](https://www.rinf.tech/bare-metal-firmware-development-what-when-and-how/)

1. Firmware Guides | Omi AI – Page 74, accessed May 8, 2025, [https://www.omi.me/blogs/firmware-guides?page=74](https://www.omi.me/blogs/firmware-guides?page=74)

1. Integrating AI/ML in Embedded Systems: A Full Guide - Waverley, accessed May 8, 2025, [https://waverleysoftware.com/blog/embedded-ai-systems-guide/](https://waverleysoftware.com/blog/embedded-ai-systems-guide/)

1. open-power/hostboot: System initialization firmware for Power systems - GitHub, accessed May 8, 2025, [https://github.com/open-power/hostboot](https://github.com/open-power/hostboot)

1. Code Firmware Faster with AI - Flux, accessed May 8, 2025, [https://www.flux.ai/p/blog/code-firmware-faster-with-ai](https://www.flux.ai/p/blog/code-firmware-faster-with-ai)

1. Can literally anyone make an AI from scratch, or do you need certain hardware and software and firmware to actually create an artificial intelligence? If so, what exactly do you need to make one? - Quora, accessed May 8, 2025, [https://www.quora.com/Can-literally-anyone-make-an-AI-from-scratch-or-do-you-need-certain-hardware-and-software-and-firmware-to-actually-create-an-artificial-intelligence-If-so-what-exactly-do-you-need-to-make-one](https://www.quora.com/Can-literally-anyone-make-an-AI-from-scratch-or-do-you-need-certain-hardware-and-software-and-firmware-to-actually-create-an-artificial-intelligence-If-so-what-exactly-do-you-need-to-make-one)

1. HostCircle BVAdvantages of Large Memory in Bare Metal Servers, accessed May 8, 2025, [https://hostcircle.nl/advantages-of-large-memory-bare-metal-servers.php](https://hostcircle.nl/advantages-of-large-memory-bare-metal-servers.php)

1. Maximizing Performance and Control with Bare Metal Servers - OpenMetal, accessed May 8, 2025, [https://openmetal.io/resources/blog/maximizing-performance-control-bare-metal-servers/](https://openmetal.io/resources/blog/maximizing-performance-control-bare-metal-servers/)

1. PC running software without OS - EEVblog, accessed May 8, 2025, [https://www.eevblog.com/forum/chat/pc-running-software-without-os/](https://www.eevblog.com/forum/chat/pc-running-software-without-os/)

1. Bare Metal Cloud: What Is It, How It Works & Main Challenges | V2 Cloud, accessed May 8, 2025, [https://v2cloud.com/glossary/bare-metal-cloud-definition](https://v2cloud.com/glossary/bare-metal-cloud-definition)

1. Why a bare-metal developer moved to operating systems - Embedded, accessed May 8, 2025, [https://www.embedded.com/why-a-bare-metal-developer-moved-to-operating-systems/](https://www.embedded.com/why-a-bare-metal-developer-moved-to-operating-systems/)

1. RTOS vs Bare-Metal - EmbeddedRelated.com, accessed May 8, 2025, [https://www.embeddedrelated.com/thread/5762/rtos-vs-bare-metal](https://www.embeddedrelated.com/thread/5762/rtos-vs-bare-metal)

1. Help a beginner understand the pros and cons of bare-metal devices, RTOS devices vs. embedded Linux devices - Reddit, accessed May 8, 2025, [https://www.reddit.com/r/embedded/comments/ldvcqo/help_a_beginner_understand_the_pros_and_cons_of/](https://www.reddit.com/r/embedded/comments/ldvcqo/help_a_beginner_understand_the_pros_and_cons_of/)

1. Does bare-metal programming have a future? : r/embedded - Reddit, accessed May 8, 2025, [https://www.reddit.com/r/embedded/comments/1awfxvg/does_baremetal_programming_have_a_future/](https://www.reddit.com/r/embedded/comments/1awfxvg/does_baremetal_programming_have_a_future/)

1. Overcoming Common Challenges of Deploying Bare Metal IaaS - Datacenters.com, accessed May 8, 2025, [https://www.datacenters.com/news/overcoming-common-challenges-of-deploying-bare-metal-iaas](https://www.datacenters.com/news/overcoming-common-challenges-of-deploying-bare-metal-iaas)

1. How Bare Metal Virtualization Is Changing The Game For High-Performance Applications, accessed May 8, 2025, [https://edgeuno.com/how-bare-metal-virtualization-is-changing-the-game-for-high-performance-applications/](https://edgeuno.com/how-bare-metal-virtualization-is-changing-the-game-for-high-performance-applications/)

\*\*

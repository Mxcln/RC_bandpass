# llm4eda

## Project Overview
This project is designed for the llm4eda class and involves simulating an RC bandpass filter using ngspice. The project utilizes agents to calculate and parse outputs, generating netlists for simulation.

## Setup&Run Instructions
1. **Clone the repository**
   ```bash
   git clone git@github.com:Zhuangjizzz/llm4eda.git
   cd llm4eda
   ```

2. **Install dependencies**
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**
   Create a `.env` file in the root directory and configure necessary environment variables if required.

## Usage
1. **Run the Simulation**
   Execute the main script to start the simulation process:
   ```bash
   python main.py
   ```
   Follow the prompts to input the desired center frequency and bandwidth for the RC bandpass filter.

2. **使用配置文件**
   现在支持通过配置文件`config.json`设置参数，您可以：
   - 自定义配置文件路径：`python main.py --config your_config.json`
   - 直接通过命令行参数指定参数：
     ```bash
     python main.py --center 200 --bandwidth 50 --r1 2000 --r2 1500 --output my_filter.cir
     ```
   - 如果不指定配置文件，将使用当前目录下的`config.json`或默认参数

3. **配置参数说明**
   配置文件支持以下参数：
   ```json
   {
       "center_frequency": 100,   // 中心频率(Hz)
       "bandwidth": 40,           // 带宽(Hz)
       "netlist_file_path": "rc_bandpass.cir",  // 输出网表文件名
       "resistance": {
           "R1": 1000,            // 高通滤波器电阻(欧姆)
           "R2": 1000             // 低通滤波器电阻(欧姆)
       },
       "capacitance": {
           "C1": null,            // 高通滤波器电容(计算得出)
           "C2": null             // 低通滤波器电容(计算得出)
       }
   }
   ```

4. **Simulation Process**
   - The `calculation_process` function uses `CalculationAgent` to compute results based on system and human prompts.
   - The `output_process` function parses the results and generates a netlist using `OutputParserAgent`.
   - The `run_simulation` function executes the ngspice simulation on the generated netlist.

5. **User Interaction**
   After each simulation, you will be prompted to confirm if the results are satisfactory. You can adjust the parameters and rerun the simulation if needed.
   修改参数后，最终的配置将自动保存到`config.json`文件中，便于下次使用。
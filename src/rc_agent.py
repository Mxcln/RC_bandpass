import os
from config import Config
from utils import read_user_prompt, read_sys_prompt, time_decorator, write_netlist
from design_agent import DesignAgent
from parse_agent import ParseAgent
from loguru import logger

class RCAgent:
    def __init__(self, config: Config):
        self.config = config

    def run(self):
        while True:
            # 执行计算过程
            logger.info("开始设计过程...")
            result = self.design_process()
            # 解析输出并生成网表
            logger.info("开始解析过程...")
            self.parse_process(result)
            # 运行仿真
            logger.info("开始仿真过程...")
            self.run_simulation()
            logger.info("仿真完成！您可以在当前目录下找到仿真结果文件 rc_bandpass.cir， 在logs目录下找到仿真日志文件。")
            # 询问用户是否满意仿真结果
            user_choice = input("\n您对仿真结果满意吗？(y/n): ")
            if user_choice.lower() == 'y':
                print("设计完成！")
                # 保存最终的配置
                self.config.save_config()
                break
            else:
                # 显示当前配置
                print(f"\n当前配置：")
                print(f"中心频率: {self.config['center_frequency']} Hz")
                print(f"带宽: {self.config['bandwidth']} Hz")
                print(f"高通电阻(R1): {self.config['resistance']['R1']} Ω")
                print(f"低通电阻(R2): {self.config['resistance']['R2']} Ω")
                
                # 允许用户修改参数
                try:
                    new_center = float(input(f"请输入新的中心频率(当前: {self.config['center_frequency']}): ") or self.config['center_frequency'])
                    new_bandwidth = float(input(f"请输入新的带宽(当前: {self.config['bandwidth']}): ") or self.config['bandwidth'])
                    new_r1 = float(input(f"请输入新的高通电阻R1(当前: {self.config['resistance']['R1']}): ") or self.config['resistance']['R1'])
                    new_r2 = float(input(f"请输入新的低通电阻R2(当前: {self.config['resistance']['R2']}): ") or self.config['resistance']['R2'])
                    
                    # 更新配置
                    config_updates = {
                        "center_frequency": new_center,
                        "bandwidth": new_bandwidth,
                        "resistance": {
                            "R1": new_r1,
                            "R2": new_r2
                        }
                    }
                    self.config.update_config(config_updates)
                    print("参数已更新！")
                except ValueError:
                    print("输入无效，使用原参数继续...")


    @time_decorator
    def design_process(self):
        center_frequency = self.config["center_frequency"]
        bandwidth = self.config["bandwidth"]
        design_sys_prompt = self.config["design_sys_prompt"]
        design_user_prompt = self.config["design_user_prompt"]
        
        sys_prompt = read_sys_prompt(design_sys_prompt)
        user_prompt = read_user_prompt(design_user_prompt, center_frequency=center_frequency, bandwidth=bandwidth)

        # 传入config到DesignAgent
        design_agent = DesignAgent(sys_prompt, self.config)
        result = design_agent.invoke(user_prompt)
        return result

    @time_decorator
    def parse_process(self, result):
        netlist_file_path = self.config["netlist_file_path"]
        parse_prompt = self.config["parse_prompt"]
        
        sys_prompt = read_sys_prompt(parse_prompt)
        # 传入config到ParseAgent
        parse_agent = ParseAgent(sys_prompt, self.config)
        netlist = parse_agent.invoke({"role":"user","content":result})
        write_netlist(netlist, netlist_file_path)

    @time_decorator
    def run_simulation(self):
        # netlist_file_path = self.config["netlist_file_path"]
        
        # print(f"\n正在运行ngspice仿真 {netlist_file_path}...")
        # os.system(f"ngspice {netlist_file_path}")
        print("仿真完成！")
    
    
        
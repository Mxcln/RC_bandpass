import sys
import argparse
import os
import json
from loguru import logger

class Config:
    def __init__(self, config_path=None, log_level=None, log_rotation=None):
        """初始化配置系统
        
        Args:
            config_path: 滤波器配置文件路径，如果为None则使用默认路径
            log_level: 日志级别，如果为None则使用默认值"INFO"
            log_rotation: 日志轮转设置，如果为None则使用默认值"5 MB"
        """
        # 设置日志系统
        self.log_level = log_level if log_level else "TRACE"
        self.log_rotation = log_rotation if log_rotation else '5 MB'
        self.file_handler_id = logger.add('logs/file_{time}.log', 
                                         format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} - {message}", 
                                         level=self.log_level,
                                         rotation=self.log_rotation,
                                         encoding='utf-8')
        
        # 加载滤波器配置
        self.config_path = config_path if config_path else "config.json"
        self.config = self._load_config()

        args = self.parse_arguments()
        self.update_config_from_args(args)

    def _load_config(self):
        """从JSON文件加载配置"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                logger.info(f"已从 {self.config_path} 加载配置")
                return config
            else:
                logger.warning(f"配置文件 {self.config_path} 不存在，使用默认配置")
                return self._default_config()
        except Exception as e:
            logger.error(f"加载配置文件出错: {str(e)}，使用默认配置")
            return self._default_config()
    
    def _default_config(self):
        """返回默认配置"""
        return {
            "center_frequency": 100,
            "bandwidth": 40,
            "netlist_file_path": "rc_bandpass.cir",
            "resistance": {
                "R1": 1000,  # 高通滤波器电阻，单位：欧姆
                "R2": 1000   # 低通滤波器电阻，单位：欧姆
            },
            "capacitance": {
                "C1": None,  # 高通滤波器电容，由公式计算得出
                "C2": None   # 低通滤波器电容，由公式计算得出
            }
        }
    
    

    def parse_arguments(self):
        """解析命令行参数"""
        parser = argparse.ArgumentParser(description='RC带通滤波器设计工具')
        parser.add_argument('--config', type=str, help='配置文件路径', default=None)
        parser.add_argument('--center', type=float, help='中心频率(Hz)', default=None)
        parser.add_argument('--bandwidth', type=float, help='带宽(Hz)', default=None)
        parser.add_argument('--r1', type=float, help='高通滤波器电阻(欧姆)', default=None)
        parser.add_argument('--r2', type=float, help='低通滤波器电阻(欧姆)', default=None)
        parser.add_argument('--output', type=str, help='输出网表文件名', default=None)
        
        return parser.parse_args()
    
    def save_config(self, config_path=None):
        """保存配置到JSON文件
        
        Args:
            config_path: 配置文件保存路径，如果为None则使用当前路径
        """
        save_path = config_path if config_path else self.config_path
        try:
            with open(save_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            logger.info(f"配置已保存到 {save_path}")
            return True
        except Exception as e:
            logger.error(f"保存配置文件出错: {str(e)}")
            return False
    
    def update_config(self, new_config):
        """更新配置
        
        Args:
            new_config: 新的配置字典
        """
        self.config.update(new_config)

    def update_config_from_args(self, args):
        """根据命令行参数更新配置"""
        config_updates = {}
        if args.center is not None:
            config_updates["center_frequency"] = args.center
        if args.bandwidth is not None:
            config_updates["bandwidth"] = args.bandwidth
        if args.output is not None:
            config_updates["netlist_file_path"] = args.output
        if args.r1 is not None:
            if "resistance" not in config_updates:
                config_updates["resistance"] = config.config["resistance"].copy()
            config_updates["resistance"]["R1"] = args.r1
        if args.r2 is not None:
            if "resistance" not in config_updates:
                config_updates["resistance"] = config.config["resistance"].copy()
            config_updates["resistance"]["R2"] = args.r2
        if config_updates:
            config.update_config(config_updates)
    
    def remove_logger(self):
        """移除日志处理器"""
        logger.remove(self.file_handler_id)
    
    def __getitem__(self, key):
        """通过字典方式访问配置项
        
        Args:
            key: 配置键名
            
        Returns:
            配置值
        """
        return self.config.get(key)

if __name__ == "__main__":
    config = Config()
    logger.info("测试配置系统")
    # 输出当前配置
    logger.info(f"当前滤波器配置: {config.config}")
    # 保存默认配置
    config.save_config()
    # 演示通过字典方式访问配置
    logger.info(f"中心频率: {config['center_frequency']}")
    logger.info(f"带宽: {config['bandwidth']}")
    logger.info(f"高通电阻: {config['resistance']['R1']}")
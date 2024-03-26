import torch
import logging
from config import Config
from models import LeftRightModel,choose_optimizer
from loader import load_data
import numpy as np
from config import Config
from evaluate import Evaluator
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main(config):

    #定义模型
    left_right_model = LeftRightModel(config)

    #选择优化器
    optim = choose_optimizer(left_right_model,config['learning_rate'],config)

    #获取训练数据
    train_data = load_data(config,config['train_data_path'])

    #测试器
    evaluator = Evaluator(left_right_model,config)

    #cuda
    cuda_avaiable = torch.cuda.is_available()
    if cuda_avaiable:
        logger.info("gpu可以使用，迁移模型至gpu")
        left_right_model=left_right_model.cuda()

    #训练
    for epoch in range(config['num_epochs']):
        left_right_model.train()
        loss_watch = []
        for i,batch_data in enumerate(train_data):

            optim.zero_grad()

            if cuda_avaiable:
                batch_data = [x.cuda() for x in batch_data]
            input_ids,target,attn_mask = batch_data
            # print('::',input_ids.shape,target.shape,attn_mask.shape)
            loss = left_right_model(input_ids,attn_mask,target)

            loss.backward() #梯度下降
            optim.step() #更新参数

            loss_watch.append(loss.item())

            if i % 50 == 0:
                logger.info("Epoch:{} Iteration:{} Loss:{}".format(epoch,i,loss.item()))
                evaluator.eval(epoch,logger,'今天下午，中新网创业精英荟来到北京石榴中心举办了活动，众多潮流公司展示了潮人健身日常：平衡车、攀岩、智能单车…小编为大家采访到攻防箭的工作人员，给大家展示时下最潮的健身方式——射箭！你会考虑这种方式健身吗？秒拍视频')



if __name__ == '__main__':
    main(Config)
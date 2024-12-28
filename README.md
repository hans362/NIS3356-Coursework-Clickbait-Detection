# NIS3356 大作业：微信公众号和今日头条标题党内容识别

## 模型下载

中文词向量模型使用 https://github.com/Embedding/Chinese-Word-Vectors，来源：Shen Li, Zhe Zhao, Renfen Hu, Wensi Li, Tao Liu, Xiaoyong Du, Analogical Reasoning on Chinese Morphological and Semantic Relations, ACL 2018.

`.model` 和 `.model.vectors.npy` 文件下载链接：https://pan.sjtu.edu.cn/web/share/a678cebcdf9fd541930e8a7a27a07e09

下载完成后放置在项目根目录下。

## 运行

```bash
pip install -r requirements.txt
python wechat.py # 微信公众号
python toutiao.py # 今日头条
```
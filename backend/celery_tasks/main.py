from celery import Celery
import os

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoStore.settings')

# 创建Celery应用
# 参数1：路径
app = Celery('celery_tasks')

# 2.设置broker
# 通过加载Django配置来设置broker地址
app.config_from_object('celery_tasks.config')

# 3.加载任务
# 参数1：任务模块列表,列表中的每个元素都是一个字符串,字符串表示一个任务模块的路径
app.autodiscover_tasks(['celery_tasks.sms'])
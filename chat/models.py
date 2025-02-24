


from django.db import models

class ChatMessage(models.Model):
    MODEL_CHOICES = (
        ('deepseek-r1:70b', '满血 DeepSeek'),
        ('deepseek-r1', '蒸馏 DeepSeek'),
    )

    user = models.CharField(max_length=100, default='Anonymous')  # 用户名，默认值可修改
    user_message = models.TextField()  # 用户输入的消息
    ai_response = models.TextField()  # AI 的响应
    model_used = models.CharField(max_length=50, choices=MODEL_CHOICES, default='deepseek-r1:70b')  # 使用的模型
    timestamp = models.DateTimeField(auto_now_add=True)  # 发送时间

    def __str__(self):
        return f"{self.user} (使用 {self.model_used}): {self.user_message} -> {self.ai_response[:50]}..."

    class Meta:
        ordering = ['-timestamp']  # 按时间降序排序（最新消息在最上面）       
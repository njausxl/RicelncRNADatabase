# 聊天视图（新增）
import os
import random
import string
import subprocess
from django.shortcuts import render
from django.db import connection
from django.http import StreamingHttpResponse
from django.views import View
from django.conf import settings
import openai
import logging
class ChatView(View):
    def get(self, request):
        model_names = {
            'full': '满血 DeepSeek',
            'chat': '蒸馏 DeepSeek'
        }
        return render(request, 'chat/chat.html', {
            'models': model_names
        })

    def post(self, request):
        user_input = request.POST.get('message')
        selected_model = request.POST.get('model', 'full')  # 默认使用 “满血 DeepSeek”

        conversation_history = request.session.get('conversation_history', [])

        # 记录用户输入
        conversation_history.append({"role": "user", "content": user_input})

        # 调用 DeepSeek API
        def generate():
            try:
                model_config = settings.AVAILABLE_MODELS[selected_model]
                client = openai.OpenAI(
                    api_key=settings.API_KEY,
                    base_url=model_config['base_url']
                )
                
                completion = client.chat.completions.create(
                    model=model_config['model_name'],
                    temperature=0.6,
                    messages=conversation_history,
                    stream=True
                )

                response_text = ""  # 存储 AI 回复

                for chunk in completion:
                    if hasattr(chunk.choices[0].delta, "reasoning_content") and chunk.choices[0].delta.reasoning_content:
                        content = chunk.choices[0].delta.reasoning_content
                    else:
                        content = chunk.choices[0].delta.content
                    if content:
                        response_text += content
                        yield content  # 流式输出到前端

                # 记录 AI 回复
                if response_text:
                    conversation_history.append({"role": "assistant", "content": response_text})
                    request.session['conversation_history'] = conversation_history

                    # 保存到数据库（如果定义了 ChatMessage 模型）
                    from .models import ChatMessage  # 动态导入以避免循环引用
                    try:
                        ChatMessage.objects.create(
                            user='Anonymous',
                            user_message=user_input,
                            ai_response=response_text,
                            model_used=model_config['model_name']
                        )
                    except Exception as e:
                        logger.error(f"数据库保存错误: {str(e)}")

            except openai.AuthenticationError as e:
                logger.error(f"认证错误: {str(e)}")
                yield f"Error: 认证失败，请检查 API 密钥 - {str(e)}"
            except openai.APIError as e:
                logger.error(f"API 错误: {str(e)}")
                yield f"Error: API 错误，模型可能不可用 - {str(e)}"
            except Exception as e:
                logger.error(f"未知错误: {str(e)}")
                yield f"Error: {str(e)}"

        return StreamingHttpResponse(generate(), content_type='text/event-stream')
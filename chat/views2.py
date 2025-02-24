import openai
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views import View
from django.conf import settings
from .models import ChatMessage  # 导入模型

class ChatView(View):
    def get(self, request):
        # 提供模型选择选项
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
                    model=model_config['model_name'],  # 使用选中的模型
                    temperature=0.6,
                    messages=conversation_history,
                    stream=True  # 开启流式输出
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

                    # 保存到数据库
                    ChatMessage.objects.create(
                        user='Anonymous',  # 可以使用 request.user 或其他标识
                        user_message=user_input,
                        ai_response=response_text,
                        model_used=model_config['model_name']
                    )

            except Exception as e:
                yield f"Error: {str(e)}"

        return StreamingHttpResponse(generate(), content_type='text/event-stream')

# 确保安装 openai 库
# pip install openai
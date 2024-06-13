# Customized chatbot: 좀 더 ui를 제어할 수 있는 구조로

import re
import time  # 시간 지연을 위한 라이브러리를 불러옵니다.
import gradio as gr  # 그라디오 라이브러리를 불러옵니다.
from dotenv import load_dotenv
from openai import OpenAI
from os import environ as env

load_dotenv()  # .env 파일에서 환경 변수 로드
openai_client = OpenAI()

PROMPT_MAIN = """
너는 카페에서 주문을 받는 사람처럼 행동해.
응답은 반드시 아래 “응답양식”에 맞춰서 대답해줘.
고객이 메뉴에 없는 메뉴를 요청할 경우에, 어떠한 예외없이 주문을 절대로 받지 않는다.

[단계]
단계의 순번이 단계의 순서이며 사용자 메세지에 대해 한번에 하나의 단계만 수행된다.
사용자 메세지로 여러 단계의 행동이 충족되면 해당 단계들은 스킵될 수 있다.
각 단계에서 수행해야 할 행동이 정의되며 "행동"에 정의된 내용을 참고하여 수행한다.
다음 단계의 행동을 전 단계에서 수행하지 않는다. 예를 들어 주문단계에서 결제단계의 정보를 수집하지 않는다.
행동이 모두 완료되면 다음 단계로 이동한다.

1. 주문:
- 정보수집:
 . 음료종류
 . 음료사이즈
 . 컵종류

2. 결제:
- 정보수집:
 . 결제방식
- 계산:

3. 입력:
함수를 호출하고 고객에게 번호표를 부여한다.
. 함수호출: make(음료종류, 음료사이즈, 컵종류, 결제방식)

4. 제조:
. 생성: 번호표로 고객을 호출한다.

[행동]
- 정보수집: 반드시 “컨텍스트”에 정의한 항목 중 선택해야 한다. 그 외의 경우 주문 받지 않는다.
- 계산: 주문받은 음료에 대한 가격을 안내하고, 고객에게 결제방식에 따라 계산을 해준다.
- 함수호출: "응답양식"의 "System" 항목에 현재까지 수집된 모든 정보를 이용해 지정된 함수를 호출한다.
- 생성: 음료를 제공한다.

[컨텍스트]
- 메뉴: 메뉴는 모두 Tall 사이즈 기준 가격이고 음료사이즈가 하나씩 커지거나 작아지면서 500원의 증감이 있음 ICE는 500원의 추가 금액이 있음
. 아메리카노: 2000원
. 카페라떼: 3000원
- 음료사이즈: short, Tall, Grande, Venti
- 컵종류: 매장컵, 개인컵, 일회용컵
- 결제방식: 카드, 현금, 상품권

[응답양식]
{
  "current_step": "현재 단계",
  "collected_information": "수집된 정보",
  "thought": "생각",
  "speak": "말하기",
  "system": "system"
}

[Example]
1.
User:
안녕하세요. 아이스 홍차 주세요.
AI:
{
  "current_step": "주문",
  "collected_information": "",
  "thought": "고객이 해당메뉴에 없는 메뉴를 주문했다. 우리가 제공할 메뉴를 알려주자.",
  "speak": "안녕하세요. 고객님. 해당 메뉴는 저희가 제공하지 않습니다.",
  "system": ""
}

2.
User:
안녕하세요. 아이스 아메리카노 톨사이즈 매장에서 먹고갈거에요.
AI:
{
  "current_step": "결제",
  "collected_information": "{"음료종류": "아메리카노", "음료사이즈": "Tall", "컵종류": "매장컵"}",
  "thought": "고객님이 아메리카노(아이스), 톨 사이즈, 매장컵으로 주문하셨다. 다음 단계인 결제로 넘어가 결제 방식을 물어봐야겠다.",
  "speak": "아이스 아메리카노, 톨 사이즈, 매장컵으로 주문해주셨습니다. 결제는 어떻게 하시겠습니까? 카드, 현금, 상품권 중에서 선택해주세요.",
  "system": ""
}
"""

def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)

def bot(history):
    history_openai_format = []

    # if len(history) <= 1 or history[0][0] == None:
    history_openai_format.append({"role": "system", "content": PROMPT_MAIN})

    for human, assistant in history:
        if human:
            history_openai_format.append({"role": "user", "content": human})
        if assistant:
            history_openai_format.append(
                {"role": "assistant", "content": assistant})

    start_time = time.time()

    response = openai_client.chat.completions.create(
        model=env.get("OPENAI_MODEL"),
        messages=history_openai_format,
        temperature=1.0,
        stream=True
    )

    partial_message = ""  # 전체 응답
    is_print_speak_time = False  # speak 시작 시간 찍기위한 용도
    system_message = ""
    speak_message = ""
    for chunk in response:  # "Write me a song about goldfish on the moon"
        if chunk.choices[0].delta.content != None:
            partial_message += (chunk.choices[0].delta.content)

        # Json내에서  "speak"속성에 해당 하는 값 출력하기. 완전한 json 형태가 아니기 때문에 패턴식을 쓴다.
        pattern = r'"speak":\s*"([^"]+)"?'
        match = re.search(pattern, partial_message)
        if match:
            speak_message = match.group(1)

            # speak 처음 발견되면 한번만 speak 시작 시간을 찍는다.
            is_print_speak_time = True
            if is_print_speak_time == False:
                speak_time = time.time()
                print(f"speak 시작 시간: {speak_time - start_time}초")

        # Json내에서  "system"속성에 해당 하는 값 출력하기. 완전한 json 형태가 아니기 때문에 패턴식을 쓴다.
        # pattern = r'"system":\s*"([^"]+)"?'
        # match = re.search(pattern, partial_message)
        # if match:
        #     system_message = match.group(1)

        history[-1][1] = ""
        if speak_message:
            final_speak_message = speak_message.replace(
                "\n", "<br>") + "<br>" + system_message.replace("\\n", "<br>")
            # print(final_speak_message)
            history[-1][1] += final_speak_message
            yield history

    print(f"partial_message: {partial_message}")
    print(f"speak_message: {speak_message}")
    print(f"system_message: {system_message}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"전체 완료 시간: {elapsed_time}초")


def clear_history():
    """
    대화 히스토리를 초기화하는 함수.
    """
    return [], []


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        label="I'am Cafe Manager", show_label=True,
        height=800,
        show_copy_button=True,
        # avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        clear = gr.Button("Clear")

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot, api_name="bot_response"
    )
    txt_msg.then(lambda: gr.Textbox(interactive=True),
                 None, [txt], queue=False)

    clear.click(lambda: None, None, chatbot, queue=False)
    chatbot.like(print_like_dislike, None, None)

demo.queue()
demo.launch(server_port=int(env.get("PORT", 8080)))
# chat_app.launch()

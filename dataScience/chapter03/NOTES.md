# chapter03 — 코드 치트시트

설명(함수 시그니처·라인별 분석·버그 기록)은 아티팩트: https://claude.ai/code/artifact/b103ec06-33e2-4600-b5a8-3fe9a07cb5c8

`.env`: `DB_USER`/`PASSWORD`/`DSN`(chapter02와 동일) + `GEMINI_API_KEY`. 이 맥 폰트는 `AppleGothic`.

## 기본 골격 — gr.Interface
```python
def fn(input1, input2):
    ...
    return output1, output2          # 여러 개면 outputs 리스트 순서와 매칭

demo = gr.Interface(
    fn=fn,
    inputs=[gr.Number(label=...), gr.Dropdown([...], label=...)],
    outputs=[gr.Textbox(label=...), gr.Plot(label=...)],
    title=..., description=...,
)
demo.launch()
```

## 자주 쓰는 입력 컴포넌트
```python
gr.Textbox(label=..., placeholder=...)
gr.Number(label=...)
gr.Radio(["a","b","c"], label=...)
gr.Dropdown(list(d.keys()), label=...)
gr.Slider(minimum=1, maximum=10, step=1, label=...)
gr.Image(label=...)                 # 업로드 이미지 → numpy 배열로 전달
gr.File(label=..., file_types=[".csv"])   # 업로드 파일 → file.name(경로)
```

## 챗봇 — gr.ChatInterface
```python
def chat_fn(message, history):
    # history: [{"role":"user"/"assistant","content":...}, ...] (턴당 2개씩)
    ...
    return reply_text

demo = gr.ChatInterface(fn=chat_fn, title=...)
demo.launch()
```

## 직접 배치 — gr.Blocks
```python
with gr.Blocks(title=...) as demo:
    gr.Markdown("## 제목")
    with gr.Row():                   # 가로로 나란히 배치
        in1 = gr.Number(label=...)
        btn = gr.Button("실행")
    with gr.Row():
        out1 = gr.Textbox(label=...)
        out2 = gr.Plot(label=...)

    btn.click(fn=my_fn, inputs=[in1], outputs=[out1, out2])

demo.launch()
```

## DB 실시간 조회 (bind 변수, SQL 인젝션 방지)
```python
query = "SELECT * FROM T WHERE CATEGORY = :category"
with oracledb.connect(user=USER, password=PASSWORD, dsn=DSN) as conn:
    df = pd.read_sql(query, conn, params={"category": category})
```

## 표 + 그래프 동시 반환
```python
def analyze(file):
    df = pd.read_csv(file.name, encoding="utf-8-sig")
    summary = df.describe().round(2)

    fig, ax = plt.subplots(figsize=(6,4))
    ax.hist(df["col"], bins=10, color="skyblue", edgecolor="black")
    ax.set_title("분포")

    return summary, fig             # gr.DataFrame, gr.Plot 순서로 매칭
```

## LLM 연동 (모델별 role 이름 차이)
```python
# OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user"/"assistant", ...}])

# Gemini (role: assistant → model)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")
model.generate_content([{"role":"user"/"model", "parts":[text]}])
```

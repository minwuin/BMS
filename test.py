import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(layout="wide")

def get_image_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_path = r"miniproject/allaboutus/pages/classroom.png"
if os.path.exists(img_path):
    img_base64 = get_image_base64(img_path)
    img_url = f"data:image/png;base64,{img_base64}"
else:
    st.error("6floor.png 파일이 없습니다.")
    st.stop()

st.title("📍 6층 평면도 좌표 추출기 (잘림 방지)")
st.info("이미지를 클릭하면 하단에 좌표가 출력됩니다. 이 좌표를 복사해서 구역을 설정하세요.")

# HTML/JS: 이미지 클릭 시 좌표를 잡아주는 핵심 로직
# height를 넉넉하게 잡거나, CSS로 이미지 크기를 조절합니다.
html_code = f"""
<div id="wrapper" style="position: relative; display: inline-block;">
    <img id="map-img" src="{img_url}" style="width: 100%; height: auto; cursor: crosshair; border: 1px solid #ccc;">
    <div id="marker" style="position: absolute; width: 12px; height: 12px; background: red; border-radius: 50%; display: none; transform: translate(-50%, -50%); pointer-events: none; border: 2px solid white;"></div>
</div>

<p id="coord-display" style="font-family: monospace; margin-top: 10px; font-size: 16px; color: #333;">
    이미지를 클릭하여 좌표를 확인하세요.
</p>

<script>
    const img = document.getElementById('map-img');
    const marker = document.getElementById('marker');
    const display = document.getElementById('coord-display');

    img.addEventListener('click', function(e) {{
        const rect = img.getBoundingClientRect();
        
        // 클릭한 위치 계산 (이미지 내부 상대 좌표)
        const x = Math.round(e.clientX - rect.left);
        const y = Math.round(e.clientY - rect.top);
        
        // 전체 이미지 크기 대비 비율 (이미지 크기가 변해도 대응 가능하게 함)
        const xPercent = ((x / rect.width) * 100).toFixed(2);
        const yPercent = ((y / rect.height) * 100).toFixed(2);

        // 마커 표시
        marker.style.left = x + 'px';
        marker.style.top = y + 'px';
        marker.style.display = 'block';

        // 텍스트 표시
        display.innerHTML = `클릭 좌표: <b>X: ${{x}}, Y: ${{y}}</b> (비율: ${{xPercent}}%, ${{yPercent}}%)`;
        
        // Streamlit에 데이터 전송 (필요 시)
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: {{x: x, y: y, xp: xPercent, yp: yPercent}}
        }}, '*');
    }});
</script>
"""

# 컴포넌트의 height를 이미지의 예상 높이에 맞춰 넉넉히 설정 (예: 800)
# 또는 이미지 너비에 따라 유동적으로 조절
components.html(html_code, height=2000)

st.markdown("""
### 💡 구역 설정 팁
1. **프로젝트룸1**의 왼쪽 위와 오른쪽 아래를 클릭해서 좌표 범위를 확인하세요.
2. 예: `X가 300~450 사이이고 Y가 50~150 사이이면 프로젝트룸1` 이라고 정의하면 됩니다.
3. 이미지 크기가 브라우저마다 바뀔 수 있으므로, **비율(%)** 데이터를 활용하는 것이 더 정확합니다.
""")
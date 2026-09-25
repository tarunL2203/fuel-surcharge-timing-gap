from pathlib import Path
from streamlit.testing.v1 import AppTest
app=Path(__file__).resolve().parents[1]/'app/streamlit_app.py'
for page in ['Overview','Scenario explorer','Data quality','Assumptions']:
 at=AppTest.from_file(str(app)).run(timeout=30)
 at.sidebar.radio[0].set_value(page).run(timeout=30)
 assert len(at.exception)==0,at.exception
 print(page,'PASS')
# Exercise a materially different selection and confirm it renders.
at=AppTest.from_file(str(app)).run(timeout=30)
at.sidebar.selectbox[0].set_value('PADD4');at.sidebar.selectbox[1].set_value('QUARTERLY');at.sidebar.checkbox[0].set_value(True);at.run(timeout=30)
assert len(at.exception)==0,at.exception
print('PADD4 quarterly seasonal clause PASS')

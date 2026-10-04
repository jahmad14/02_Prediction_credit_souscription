import os
import sys
from streamlit.testing.v1 import AppTest

def test_bank_app():
    dep_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dep_dir)
    print(f"Testing app.py in: {dep_dir}")
    
    # 1. Test profil 1 : client standard (refus probable)
    at1 = AppTest.from_file("app.py", default_timeout=30)
    at1.run()
    assert len(at1.exception) == 0, f"Exception initialisation 1 : {at1.exception}"
    
    # Remplir le formulaire 1
    at1.number_input[0].set_value(30) # age
    at1.selectbox[0].select("blue-collar") # job
    at1.selectbox[1].select("married") # marital
    at1.selectbox[2].select("basic.4y") # education
    at1.selectbox[3].select("yes") # housing
    at1.selectbox[4].select("no") # loan
    at1.selectbox[5].select("cellular") # contact
    
    at1.selectbox[6].select("may") # month
    at1.selectbox[7].select("mon") # day_of_week
    at1.number_input[1].set_value(60) # duration
    at1.number_input[2].set_value(2) # campaign
    at1.number_input[3].set_value(999) # pdays
    at1.number_input[4].set_value(0) # previous
    at1.selectbox[8].select("nonexistent") # poutcome
    
    at1.button[0].click().run()
    assert len(at1.exception) == 0, f"Exception prédiction 1 : {at1.exception}"
    assert len(at1.warning) > 0 or len(at1.success) > 0, "Aucun résultat trouvé pour test 1"
    res1 = at1.warning[0].value if len(at1.warning) > 0 else at1.success[0].value
    print(f"Résultat Test 1 : {res1}")
    
    # 2. Test profil 2 : client très engagé (souscription probable)
    at2 = AppTest.from_file("app.py", default_timeout=30)
    at2.run()
    assert len(at2.exception) == 0, f"Exception initialisation 2 : {at2.exception}"
    
    at2.number_input[0].set_value(28) # age
    at2.selectbox[0].select("management") # job
    at2.selectbox[1].select("single") # marital
    at2.selectbox[2].select("university.degree") # education
    at2.selectbox[3].select("yes") # housing
    at2.selectbox[4].select("no") # loan
    at2.selectbox[5].select("cellular") # contact
    
    at2.selectbox[6].select("jun") # month
    at2.selectbox[7].select("wed") # day_of_week
    at2.number_input[1].set_value(900) # duration
    at2.number_input[2].set_value(1) # campaign
    at2.number_input[3].set_value(6) # pdays
    at2.number_input[4].set_value(2) # previous
    at2.selectbox[8].select("success") # poutcome
    
    at2.button[0].click().run()
    assert len(at2.exception) == 0, f"Exception prédiction 2 : {at2.exception}"
    assert len(at2.warning) > 0 or len(at2.success) > 0, "Aucun résultat trouvé pour test 2"
    res2 = at2.warning[0].value if len(at2.warning) > 0 else at2.success[0].value
    print(f"Résultat Test 2 : {res2}")
    
    assert res1 != res2, f"Les prédictions sont identiques : {res1}"
    print("SUCCESS: Bank app test passed with 0 exception and two different predictions!")

if __name__ == "__main__":
    test_bank_app()

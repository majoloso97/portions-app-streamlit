import streamlit as st
from scrapper.Scrapper import Scrapper

class App:
    def __init__(self):
        self.portions_data = self.get_portions_data()

    def get_portions_data(self):
        sc = Scrapper()
        return sc.get_data_as_df()


    def calculate_alternative_portion(self, food, unit, value, alternative, alt_unit):
        df = self.portions_data
        original_portion = df[df.Alimento == food][unit].values

        rate = value/original_portion
        alt_value = df[df.Alimento == alternative][alt_unit].values

        new_portion = alt_value * rate

        return new_portion

    
    def build_ui(self):
        st.header('Calculadora de porciones')
        st.wtrite('Esta calculadora permite convertir entre porciones equivalentes de distintos alimentos.')
        with st.form('input_form'):
            food = st.selectbox('Selecione el alimento a convertir:', self.portions_data.Alimento)
            value = st.number_input('Digite la cantidad de su porción', 0.0, 1000.0)
            unit = st.radio('Seleccione la unidad de medida de su porción', self.portions_data.columns[3:], horizontal = True)

            alternative = st.selectbox('Selecione el alimento deseado:', self.portions_data.Alimento)
            alt_unit = st.radio('Seleccione la unidad de medida deseada', self.portions_data.columns[3:], horizontal = True)

            submitted = st.form_submit_button("Submit")
        
            if submitted:
                result = self.calculate_alternative_portion(food, unit, value, alternative, alt_unit)
                st.write(f'{value} {unit} de {food} son equivalentes a {result[0].round(2)} {alt_unit} de {alternative}')
    

    def all_data(self):
        with st.expander('Ver todos los datos'):
            st.dataframe(self.portions_data.style.format(
                            subset=['taza','gramo','oz','unidad','clara','cda','ml','cdita'],
                            formatter='{:.2f}', na_rep='-'))


@st.experimental_singleton
def build(App):
    return App()

app = build(App)

app.build_ui()
app.all_data()

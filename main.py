# This is a sample Python script.
import streamlit as ts
from Individuo import *
from AGS import *
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("EJECUCIÓN DE UN MAIN")

    ts.write("AGS - PLANIFICADOR DE MATERIAS POR RESAGO")

    # CREACION DE FORMULARIO EN STREAMLIT
    form = ts.form(key="my_form")
    po = form.text_input("Ingrese PO")
    pc = form.text_input("Ingrese PC")
    epoch = form.text_input("Ingrese EPOCA")
    cu_a = form.text_input("Ingrese CUATRIMESTRE ACTUAL")
    matricula = form.text_input("Ingrese MATRICULA")
    materias = form.text_input("Ingrese MATERIAS PENDIENTES")
    submit_button = form.form_submit_button(label="Ejecutar")

    if submit_button:
        # CREACION DE INDIVIDUO
        algoritmo_g = AGS(int(epoch), float(pc),int(po), int(cu_a), int(matricula), materias)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

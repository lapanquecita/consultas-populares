import json

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots


def create_map():
    """
    Esta función crea un mapa Choropleth con la información
    de participación por entidad.
    """

    # Cargamos nuestro archivo JSON.
    data = json.load(open("./data/2021.json", "r", encoding="utf-8"))

    # Obtenemos el total nacional.
    total_nacional = data["totalVotos"]
    participacion_nacional = data["porcentajeParticipacionCiudadana"]

    subtitulo = f"Nacional: {participacion_nacional:,.2f}% ({total_nacional:,.0f} votos)"

    entidades = dict()

    # Iteramos sobre todas las entidades.
    for entidad in data["entidadesHijas"][:-1]:

        # Limpiamos el nombre de la entidad.
        nombre = entidad["nombreNodo"].title().replace("De", "de")

        if nombre == "México":
            nombre = "Estado de México"

        # Extraemos el valor que nos interesa.
        participacion = entidad["porcentajeParticipacionCiudadana"]

        entidades[nombre] = [participacion]

    # Creamos un DataFrame con los valores de nuestro diccionario.
    df = pd.DataFrame.from_dict(
        entidades, orient="index", columns=["participacion"])

    ubicaciones = list()
    valores = list()

    marcas = np.arange(3, 11.5 + 0.5, 0.85)
    etiquetas = list()

    for marca in marcas:
        etiquetas.append(f"{marca:,.1f}%")

    geojson = json.load(open("./mexico.json",  "r", encoding="utf-8"))

    # Iteramos sobre las entidades dentro del GeoJSON.
    for item in geojson["features"]:
        geo = item["properties"]["ADMIN_NAME"]
        ubicaciones.append(geo)
        valores.append(df.loc[geo, "participacion"])

    fig = go.Figure()

    fig.add_traces(
        go.Choropleth(
            geojson=geojson,
            locations=ubicaciones,
            z=valores,
            featureidkey="properties.ADMIN_NAME",
            colorscale="portland",
            colorbar=dict(
                x=0.03,
                y=0.5,
                ypad=50,
                ticks="outside",
                outlinewidth=2,
                outlinecolor="#FFFFFF",
                tickvals=marcas,
                ticktext=etiquetas,
                tickwidth=3,
                tickcolor="#FFFFFF",
                ticklen=10,
                tickfont_size=20
            ),
            marker_line_color="white",
            marker_line_width=1.25,
            zmin=3.0,
            zmax=11.5
        )
    )

    fig.update_geos(
        fitbounds="geojson",
        showocean=True,
        oceancolor="#082032",
        showcountries=False,
        framecolor="#FFFFFF",
        framewidth=2,
        showlakes=False,
        coastlinewidth=0,
        landcolor="#1C0A00"
    )

    fig.update_layout(
        showlegend=False,
        font_family="Quicksand",
        font_color="#FFFFFF",
        margin={"r": 40, "t": 50, "l": 40, "b": 30},
        width=1280,
        height=720,
        paper_bgcolor="#334756",
        annotations=[
            dict(
                x=0.0275,
                y=0.45,
                textangle=-90,
                xanchor="center",
                yanchor="middle",
                text="Proporción relativa al padrón electoral por entidad",
                font_size=16
            ),
            dict(
                x=0.5,
                y=1.0,
                xanchor="center",
                yanchor="top",
                text="Distribución por entidad del porcentaje de participación en la consulta popular del año 2021 en México",
                font_size=24
            ),
            dict(
                x=0.01,
                y=-0.03,
                xanchor="left",
                yanchor="top",
                text="Fuente: INE (2021)",
                font_size=22
            ),
            dict(
                x=0.5,
                y=-0.03,
                xanchor="center",
                yanchor="top",
                text=subtitulo,
                font_size=22
            ),
            dict(
                x=1.01,
                y=-0.03,
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
                font_size=22
            )
        ]
    )

    fig.write_image("./1.png")


def create_table():
    """
    Esta función crea 2 tablas, cada una contiene
    información de 16 entidades de México.
    """

    # Cargamos nuestro archivo JSON.
    data = json.load(open("./data/2021.json", "r", encoding="utf-8"))

    entidades = dict()

    # Iteramos sobre todas las entidades.
    for entidad in data["entidadesHijas"][:-1]:

        # Limpiamos el nombre de la entidad.
        nombre = entidad["nombreNodo"].title().replace("De", "de")

        if nombre == "México":
            nombre = "Estado de México"

        # Extraemos los valores que nos interesa.
        participacion = entidad["porcentajeParticipacionCiudadana"]
        total_votos = entidad["totalVotos"]

        entidades[nombre] = [participacion, total_votos]

    # Creamos un DataFrame con los valores de nuestro diccionario.
    df = pd.DataFrame.from_dict(
        entidades, orient="index", columns=["participacion", "total"])

    # ordenamos por participación de mayor a menor.
    df.sort_values("participacion", ascending=False, inplace=True)

    # Creamos un lienzo con dos subplots de tipo Table.
    fig = make_subplots(
        rows=1,
        cols=2,
        horizontal_spacing=0.03,
        specs=[
            [
                {"type": "table"},
                {"type": "table"}
            ]
        ]
    )

    # La primera tabla cubre las primers 16 entidades.
    fig.add_trace(
        go.Table(
            columnwidth=[110, 80],
            header=dict(
                values=[
                    "<b>Entidad</b>",
                    "<b>Votos</b>",
                    "<b>Participación ↓</b>"
                ],
                font_color="white",
                fill_color="#ff5722",
                align="center",
                height=32,
                line_width=0.8),
            cells=dict(
                values=[
                    df.index[:16],
                    df["total"][:16],
                    df["participacion"][:16]
                ],
                fill_color="#082032",
                height=32,
                suffix=["", "", "%"],
                format=["", ",", ".2f"],
                line_width=0.8,
                align=["left", "center"]
            )
        ), col=1, row=1
    )

    # La segunda tabla cubre las últimas 16 entidades.
    fig.add_trace(
        go.Table(
            columnwidth=[110, 80],
            header=dict(
                values=[
                    "<b>Entidad</b>",
                    "<b>Votos</b>",
                    "<b>Participación ↓</b>"
                ],
                font_color="white",
                fill_color="#ff5722",
                align="center",
                height=32,
                line_width=0.8),
            cells=dict(
                values=[
                    df.index[16:],
                    df["total"][16:],
                    df["participacion"][16:]
                ],
                fill_color="#082032",
                height=32,
                suffix=["", "", "%"],
                format=["", ",", ".2f"],
                line_width=0.8,
                align=["left", "center"]
            )
        ), col=2, row=1
    )

    fig.update_layout(
        showlegend=False,
        width=1280,
        height=570,
        font_family="Quicksand",
        font_color="white",
        font_size=20,
        title="",
        title_x=0.5,
        title_y=0.95,
        margin_t=0,
        margin_l=40,
        margin_r=40,
        margin_b=0,
        title_font_size=26,
        paper_bgcolor="#334756"
    )

    fig.write_image("./2.png")


def combine_images():
    """
    Esta función va a combianr nuestro mapa y tabla en una sola imagen.
    """

    # Cargamos las imágenes.
    image1 = Image.open("./1.png")
    image2 = Image.open("./2.png")

    # Calculos el ancho y el alto de la nueva imagen.
    result_width = image1.width
    result_height = image1.height + image2.height

    # Copiamos los pixeles de nuestras imágenes en nuestro nueov lienzo.
    result = Image.new("RGB", (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(0, image1.height))

    # Guardamos la nueva imagen.
    result.save("./2021.png")


if __name__ == "__main__":

    create_map()
    create_table()
    combine_images()

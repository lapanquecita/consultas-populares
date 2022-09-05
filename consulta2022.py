import json

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def main():

    # Cargamos nuestro archivo JSON.
    data = json.load(open("./data/2022.json", "r", encoding="utf-8"))

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

    marcas = np.arange(9, 36.0 + 3.0, 3.0)
    etiquetas = list()

    for marca in marcas:
        etiquetas.append(f"{marca:,.0f}%")

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
            colorbar={"x": 0.03, "y": 0.5, "ypad": 50, "ticks": "outside", "outlinewidth": 2,
                      "outlinecolor": "#FFFFFF", "tickvals": marcas, "ticktext": etiquetas,
                      "tickwidth": 3, "tickcolor": "#FFFFFF", "ticklen": 10, "tickfont_size": 20},
            marker_line_color="white",
            marker_line_width=1.25,
            zmin=9.0, zmax=36.0
        )
    )

    fig.update_geos(
        fitbounds="geojson", showocean=True, oceancolor="#082032",
        showcountries=False, framecolor="#FFFFFF", framewidth=2,
        showlakes=False, coastlinewidth=0, landcolor="#1C0A00"
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
                text="Distribución por entidad del porcentaje de participación en la consulta popular del año 2022 en México",
                font_size=24
            ),
            dict(
                x=0.01,
                y=-0.03,
                xanchor="left",
                yanchor="top",
                text="Fuente: INE (2022)",
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

    fig.write_image("./2022.png")


if __name__ == "__main__":

    main()

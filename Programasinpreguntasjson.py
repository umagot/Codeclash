import json
import re
import string

# Diccionario con historia general de provincias
infogeneral = {
    "buenos aires": "Fue fundada en 1536 por Pedro de Mendoza y refundada en 1580 por Juan de Garay. Desde el período colonial fue un puerto clave por su ubicación estratégica sobre el Río de la Plata. Fue escenario de las Invasiones Inglesas (1806–1807) y de los principales procesos revolucionarios, incluida la Revolución de Mayo en 1810. La provincia de Buenos Aires, que rodea a la ciudad, también tuvo gran protagonismo en la historia nacional, con figuras como Juan Manuel de Rosas y una economía basada en la ganadería, agricultura e industria.",
    "catamarca": "San Fernando del Valle de Catamarca fue fundada en 1683 por Fernando de Mendoza y Mate de Luna. La provincia tiene profundas raíces indígenas diaguitas y calchaquíes. Su nombre proviene del quechua 'Katamarka' que significa 'Fortaleza en la ladera'. Fue escenario de las Guerras Calchaquíes. Destaca su artesanía en telar, cuero y cerámica.",
    "chaco": "Originalmente habitada por pueblos indígenas como los qom y wichí, la provincia fue incorporada al territorio nacional en el siglo XIX y se convirtió en provincia en 1951.",
    "chubut": "La historia de Chubut comienza con los pueblos originarios, principalmente tehuelches y mapuches, que habitaron la región durante siglos antes de la llegada europea. En 1865 llegaron los colonos galeses a bordo del barco Mimosa y fundaron la primera colonia en la zona del valle del río Chubut, estableciendo un vínculo cultural que aún perdura. Durante el siglo XIX, el Estado argentino consolidó su control sobre el territorio a través de campañas militares como la Conquista del Desierto. Chubut fue constituido como territorio nacional en 1884 y se convirtió en provincia en 1955. A lo largo del siglo XX creció gracias a la ganadería ovina, la pesca, la industria petrolera y, más recientemente, el turismo en lugares como Puerto Madryn, Península Valdés y la cordillera andina. Su identidad se destaca por la convivencia de culturas originarias, criollas y galesas.",
    "cordoba": "Fundada en 1573 por Jerónimo Luis de Cabrera, Córdoba es una de las ciudades más antiguas de Argentina. Durante la época colonial fue un centro jesuita clave, cuya Manzana Jesuítica es Patrimonio de la Humanidad. También tuvo un rol destacado en la reforma universitaria de 1918 y es hoy un polo cultural, educativo y productivo del país.",
    "corrientes": "Fundada el 3 de abril de 1588 como San Juan de Vera de las Siete Corrientes, fue una de las provincias fundadoras de la Confederación Argentina.",
    "entre rios": "Habitada originalmente por guaraníes, charrúas y chanás, la provincia fue escenario de importantes eventos durante las guerras de independencia y civiles.",
    "formosa": "Habitada por pueblos indígenas como los pilagás y wichíes, fue incorporada al territorio nacional en el siglo XIX y se convirtió en provincia en 1955.",
    "jujuy": "Jujuy es una provincia con profundas raíces indígenas, principalmente de las culturas Omaguaca, Atacama y Quechua. Fue fundada oficialmente como ciudad en 1593 por Francisco de Argañarás y Murguía, aunque la región ya tenía asentamientos indígenas desde mucho antes. Fue escenario de numerosas batallas durante la independencia, destacándose el Éxodo Jujeño liderado por Manuel Belgrano en 1812. Su identidad está marcada por la fuerte influencia andina y el mestizaje cultural.",
    "la pampa": "La Pampa fue habitada originalmente por pueblos originarios como los ranqueles y tehuelches. Durante la conquista y expansión territorial en el siglo XIX, fue escenario de enfrentamientos entre indígenas y el Estado argentino. Se constituyó como provincia en 1951. Su economía se desarrolló con la ganadería extensiva y, en menor medida, con agricultura.",
    "la rioja": "Fundada en 1591 por Juan Ramírez de Velasco. Su nombre proviene de la región homónima de España. La historia está marcada por la resistencia de los diaguitas y calchaquíes contra la colonización española y las luchas entre unitarios y federales. Destaca la figura del caudillo Facundo Quiroga. Tradiciones culturales vinculadas a la religiosidad popular.",
    "mendoza": "Mendoza fue fundada en 1561 por Pedro del Castillo. En tiempos prehispánicos estuvo habitada por los huarpes. Durante la independencia, fue clave por ser base del Ejército de los Andes liderado por José de San Martín. Su desarrollo moderno se vincula al sistema de riego y la industria vitivinícola, que es emblema de la región.",
    "misiones": "Misiones fue habitada originalmente por los guaraníes y fue escenario del establecimiento de reducciones jesuíticas en los siglos XVII y XVIII, destacándose las ruinas de San Ignacio Miní, fue declarada provincia en 1953.",
    "neuquen": "Neuquén tiene sus raíces en pueblos originarios como los mapuches, que habitaron la región antes de la llegada del Estado argentino. A fines del siglo XIX, durante la Campaña del Desierto, el gobierno nacional ocupó el territorio. En 1884 se creó como territorio nacional y en 1955 se convirtió en provincia. Su desarrollo se basó en la explotación de petróleo y gas, con un fuerte impulso en la actualidad gracias a Vaca Muerta, una de las mayores reservas no convencionales del mundo. También es importante por su energía hidroeléctrica y su turismo, con destinos como San Martín de los Andes y Villa La Angostura.",
    "rio negro": "La historia de Río Negro comienza con los pueblos originarios como los mapuches, tehuelches y pehuenches, quienes habitaban la región mucho antes de la llegada de los españoles. Durante la colonización, la zona fue de difícil acceso y permaneció relativamente aislada. A lo largo del siglo XIX, el territorio fue disputado por Argentina y Chile, y en 1955 se estableció como una provincia separada de Buenos Aires. A partir del siglo XX, Río Negro experimentó un notable desarrollo económico gracias a la irrigación de tierras, lo que permitió el crecimiento de la agricultura, especialmente la fruticultura. Además, la inmigración europea contribuyó a su expansión cultural y económica. Hoy en día, Río Negro sigue siendo una provincia clave para la economía argentina, destacándose en sectores como el turismo, con lugares como Bariloche, y la producción de energía, especialmente petróleo y gas.",
    "salta": "Conocida como 'Salta la Linda', fue fundada en 1582 por Hernando de Lerma. La provincia jugó un papel crucial en la independencia argentina, destacándose Martín Miguel de Güemes, quien defendió la frontera norte contra los realistas. Su arquitectura colonial está bien preservada, especialmente en su capital. La cultura salteña refleja una fuerte influencia española mezclada con tradiciones indígenas.",
    "san juan": "Fundada en 1562 por Juan Jufré, la provincia fue cuna de Domingo Faustino Sarmiento, figura clave en la educación argentina. San Juan fue devastada por un terremoto en 1944, lo que dio lugar a una reconstrucción moderna. Tiene fuerte herencia huarpe y una economía ligada a la vitivinicultura y la minería.",
    "san luis": "San Luis fue fundada en 1594 por Luis Jufré de Loaysa y Meneses. Su historia está marcada por la resistencia indígena de los huarpes y la posterior colonización. Durante las guerras de independencia, la provincia tuvo un rol logístico importante. En el siglo XX se consolidó como destino turístico y modelo de gestión moderna.",
    "santa cruz": "La historia de Santa Cruz comienza con los pueblos originarios como los tehuelches, quienes habitaron la región durante miles de años antes de la llegada de los europeos. En el siglo XVI, exploradores españoles como Hernando de Magallanes recorrieron la costa atlántica, aunque el territorio permaneció casi despoblado durante mucho tiempo. En el siglo XIX, con la expansión del Estado argentino hacia la Patagonia, comenzaron los asentamientos y la colonización, impulsados por la llamada 'Conquista del Desierto'. Santa Cruz se constituyó oficialmente como territorio nacional en 1884 y, más tarde, fue reconocida como provincia en 1957. Su economía creció gracias a la ganadería ovina, la minería, el petróleo y, en tiempos recientes, el turismo, especialmente en lugares como El Calafate y el glaciar Perito Moreno. Hoy es una de las provincias más importantes del sur argentino, con una rica historia ligada al desarrollo patagónico.",
    "santa fe": "Fundada en 1573, la ciudad de Santa Fe fue una de las primeras del país y desempeñó un papel clave en la historia argentina, incluyendo la firma de la Constitución Nacional en 1853.",
    "santiago del estero": "Es la provincia más antigua de Argentina, fundada en 1553 por Francisco de Aguirre. Conocida como 'Madre de Ciudades'. Fue hogar de comunidades indígenas tonocotés y juríes. Conserva el uso del quichua santiagueño, única variante del quechua en Argentina. Cuna de importantes manifestaciones culturales, especialmente música folclórica.",
    "tierra del fuego": "La historia de Tierra del Fuego comienza con los pueblos originarios yámanas, selk'nam, haush y kawésqar, que habitaron la región durante milenios adaptándose a un entorno hostil y frío. En 1520, Fernando de Magallanes fue el primer europeo en avistar estas tierras, nombrándolas 'Tierra del Humo', luego cambiada a 'Tierra del Fuego' por Carlos I de España. Durante siglos, la región permaneció aislada hasta fines del siglo XIX, cuando el Estado argentino fortaleció su presencia mediante la instalación de un presidio en Ushuaia y la expansión de la soberanía. Esto tuvo un fuerte impacto en los pueblos originarios, que fueron desplazados o exterminados. En 1884 se creó el Territorio Nacional de Tierra del Fuego y recién en 1990 fue declarado provincia, incluyendo también a las islas del Atlántico Sur y la Antártida Argentina. Hoy, Tierra del Fuego es la provincia más austral del país, con una historia marcada por el contraste entre la cultura indígena, la colonización y su crecimiento como polo turístico y estratégico.",
    "tucuman": "San Miguel de Tucumán fue fundada en 1565 por Diego de Villarroel y trasladada a su ubicación actual en 1685. Conocida como el 'Jardín de la República'. Lugar destacado en la historia argentina por ser la cuna de la independencia nacional, firmada el 9 de julio de 1816. Centro económico importante por la industria azucarera."
}

# Conjunto con palabras clave
palabrasclave = {
    "historia", "viajar", "hotel", "hospedaje", "clima", "lugares", "actividades", "moverse", "transporte"
}

# Cargar información desde archivo
def cargar(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Guardar información en el archivo (ordenada alfabéticamente)
def guardar(archivo, datos):
    # Ordenar alfabéticamente por pregunta
    datos_ordenados = sorted(datos, key=lambda x: x["pregunta"])
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos_ordenados, f, indent=2, ensure_ascii=False)

# Función para normalizar texto (quitar acentos y estandarizar)
def normalizar(texto):
    # Convertir a minúsculas y eliminar espacios extra
    texto = texto.lower().strip()
    # Eliminar signos de puntuación
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

# Comparación por palabras clave
def similitud(p1, p2):
    # Normalizar los textos para mejor comparación
    p1_norm = normalizar(p1)
    p2_norm = normalizar(p2)
    
    palabras1 = set(p1_norm.split())
    palabras2 = set(p2_norm.split())
    comunes = palabras1.intersection(palabras2)
    
    # Evitar división por cero
    if len(palabras1) == 0:
        return 0
        
    return len(comunes) / len(palabras1)

# Verificar si una pregunta ya existe en la base de datos
def pregunta_existe(pregunta, base):
    pregunta_norm = normalizar(pregunta)
    for item in base:
        if similitud(pregunta_norm, normalizar(item["pregunta"])) >= 0.8:  # Alta similitud
            return True, item["pregunta"]
    return False, None

# Buscar respuesta más parecida en base a las preguntas guardadas
def encontrarrespuesta(preguntausuario, base):
    mejor = 0
    respuesta = None
    
    for item in base:
        sim = similitud(preguntausuario, item["pregunta"])
        if sim > mejor and sim >= 0.3:  # Margen mínimo para considerar una respuesta válida
            mejor = sim
            respuesta = item["respuesta"]
    
    return respuesta

# Añadir una nueva pregunta y respuesta a la base de datos
def agregar_pregunta_respuesta(pregunta, respuesta, base, archivo):
    # Verificar si la pregunta ya existe
    existe, _ = pregunta_existe(pregunta, base)
    if existe:
        return False
    
    # Agregar la nueva pregunta y respuesta
    base.append({"pregunta": pregunta, "respuesta": respuesta})
    
    # Guardar en el archivo (ordenado alfabéticamente)
    guardar(archivo, base)
    return True

# Ejecutar chatbot
def chatbot():
    archivo = "preguntasyrespuestas.json"
    base = cargar(archivo)

    print("¡Holaaaaaaaaaaaaaaaaaa! Soy tu chatbot de viajes. Escribí 'fin' para salir.")
    
    while True:
        pregunta = input("Usuario: ").strip().lower()

        # Salir del chatbot
        if pregunta == "fin":
            print("Chatbot: ¡Hasta pronto!")
            break

        # Respuesta a saludos
        if re.search(r"hola|ola", pregunta):
            print("Chatbot: ¡Hola! ¿En qué puedo ayudarte?")
            continue

        # Si la pregunta es solo el nombre de una provincia
        if pregunta in infogeneral:
            print("Chatbot:", infogeneral[pregunta])
            continue

        # Si la pregunta contiene una palabra clave
        palabras_encontradas = [palabra for palabra in palabrasclave if palabra in pregunta.split()]
        if palabras_encontradas:
            # Intentar identificar la provincia mencionada
            provincias_mencionadas = [prov for prov in infogeneral.keys() if prov in pregunta]
            
            if provincias_mencionadas:
                # Si ya hay provincia en la pregunta
                provincia = provincias_mencionadas[0]
                # Buscar respuesta específica
                clave_busqueda = f"{palabras_encontradas[0]} {provincia}"
                respuesta = encontrarrespuesta(clave_busqueda, base)
                
                if respuesta:
                    print("Chatbot:", respuesta)
                else:
                    print(f"Chatbot: No tengo información específica sobre {palabras_encontradas[0]} en {provincia}.")
                    print("¿Te gustaría agregar esta información para futuras consultas?")
                    respuesta_usuario = input("Usuario (si/no): ").strip().lower()
                    
                    if respuesta_usuario == "si":
                        print("Chatbot: Por favor, proporciona la información:")
                        nueva_respuesta = input("Información: ").strip()
                        nueva_pregunta = f"{palabras_encontradas[0]} {provincia}"
                        
                        # Verificar si ya existe
                        existe, pregunta_similar = pregunta_existe(nueva_pregunta, base)
                        if existe:
                            print(f"Chatbot: Ya existe una pregunta similar: '{pregunta_similar}'")
                        else:
                            agregar_pregunta_respuesta(nueva_pregunta, nueva_respuesta, base, archivo)
                            print("Chatbot: ¡Gracias! He agregado esta información.")
            else:
                # No hay provincia en la pregunta, preguntar por una
                print("Chatbot: ¿De qué provincia en específico necesitas esa información?")
                provincia = input("Usuario: ").strip().lower()
                
                if provincia in infogeneral:
                    # Buscar respuesta específica
                    clave_busqueda = f"{palabras_encontradas[0]} {provincia}"
                    respuesta = encontrarrespuesta(clave_busqueda, base)
                    
                    if respuesta:
                        print("Chatbot:", respuesta)
                    else:
                        print(f"Chatbot: No tengo información específica sobre {palabras_encontradas[0]} en {provincia}.")
                        print("¿Te gustaría agregar esta información para futuras consultas?")
                        respuesta_usuario = input("Usuario (si/no): ").strip().lower()
                        
                        if respuesta_usuario == "si":
                            print("Chatbot: Por favor, proporciona la información:")
                            nueva_respuesta = input("Información: ").strip()
                            nueva_pregunta = f"{palabras_encontradas[0]} {provincia}"
                            
                            # Verificar si ya existe
                            existe, pregunta_similar = pregunta_existe(nueva_pregunta, base)
                            if existe:
                                print(f"Chatbot: Ya existe una pregunta similar: '{pregunta_similar}'")
                            else:
                                agregar_pregunta_respuesta(nueva_pregunta, nueva_respuesta, base, archivo)
                                print("Chatbot: ¡Gracias! He agregado esta información.")
                else:
                    print("Chatbot: No tengo información sobre esa provincia.")
            continue
        
        # Buscar respuesta general en el archivo
        respuesta = encontrarrespuesta(pregunta, base)
        if respuesta:
            print("Chatbot:", respuesta)
        else:
            print("Chatbot: No sé la respuesta. ¿Te gustaría agregarla para futuras consultas?")
            respuesta_usuario = input("Usuario (si/no): ").strip().lower()
            
            if respuesta_usuario == "si":
                print("Chatbot: Por favor, proporciona la respuesta:")
                nueva_respuesta = input("Respuesta: ").strip()
                
                # Verificar si la pregunta ya existe
                existe, pregunta_similar = pregunta_existe(pregunta, base)
                if existe:
                    print(f"Chatbot: Ya existe una pregunta similar: '{pregunta_similar}'")
                else:
                    agregar_pregunta_respuesta(pregunta, nueva_respuesta, base, archivo)
                    print("Chatbot: ¡Gracias! He agregado esta información.")

if __name__ == "__main__":
    chatbot()
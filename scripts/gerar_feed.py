import os
from google import genai
from google.genai import types

# 1. Verifica a chave de API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A variável GEMINI_API_KEY não foi encontrada nos Secrets.")

client = genai.Client(api_key=api_key)

prompt = """
Você é um curador de notícias especializado em tecnologia e educação.
Pesquise na web as 3 a 5 principais notícias investigativas e de alto impacto das últimas 24 horas sobre:
1. Inteligência Artificial em geral
2. Inteligência Artificial aplicada à Educação
3. Governança e regulação de tecnologia

Gere um documento XML de feed RSS 2.0 válido e completo contendo:
- <channel> com:
  * <title>: Feed IA e Educação
  * <link>: https://tirlonirs.github.io/meu-feed-ia/feed.xml
  * <description>: Resumo diário de notícias investigativas sobre IA, Educação e Tecnologia.
  * <language>: pt-BR
- Cada notícia como um <item> com:
  * <title>: título claro e objetivo.
  * <link>: URL original da matéria.
  * <guid>: a mesma URL original da matéria.
  * <pubDate>: data no padrão RFC 822 (ex: Fri, 18 Sep 2026 12:00:00 GMT).
  * <description>: resumo direto contendo o fato, o impacto a longo prazo e a citação da fonte envolto em <![CDATA[ ... ]]>.

Retorne APENAS o código XML puro, começando em <?xml version="1.0" encoding="UTF-8"?>.
Não inclua delimitadores markdown (como ```xml ou ```).
"""

# 2. Utiliza o modelo gemini-3.1-flash com a ferramenta de busca do Google
chat = client.chats.create(
    model="gemini-3.1-flash",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())]
    )
)

response = chat.send_message(prompt)
conteudo_xml = response.text.strip()

# 3. Limpeza preventiva de blocos markdown
if conteudo_xml.startswith("```xml"):
    conteudo_xml = conteudo_xml[6:]
if conteudo_xml.startswith("```"):
    conteudo_xml = conteudo_xml[3:]
if conteudo_xml.endswith("```"):
    conteudo_xml = conteudo_xml[:-3]

conteudo_xml = conteudo_xml.strip()

# 4. Salva o feed na raiz do repositório
with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(conteudo_xml)

print("feed.xml gerado e salvo com sucesso.")
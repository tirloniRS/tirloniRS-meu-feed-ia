import os
from google import genai
from google.genai import types

# Inicializa o cliente com a chave dos Secrets do GitHub
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A variável GEMINI_API_KEY não foi encontrada.")

client = genai.Client(api_key=api_key)

prompt = """
Você é um curador de notícias especializado em tecnologia e educação.
Pesquise na web as 3 a 5 principais notícias investigativas e de alto impacto das últimas 24 horas sobre:
1. Inteligência Artificial em geral
2. Inteligência Artificial aplicada à Educação
3. Governança e regulação de tecnologia

Gere um documento XML de feed RSS 2.0 válido e completo contendo:
- <channel> com título "Feed IA e Educação", link "https://tirlonirs.github.io/meu-feed-ia/feed.xml" e descrição.
- Cada notícia como um <item> com:
  * <title>: título claro e objetivo.
  * <link>: URL original da fonte da notícia.
  * <guid>: a mesma URL original da fonte.
  * <pubDate>: data no padrão RFC 822 (ex: Fri, 18 Sep 2026 12:00:00 GMT).
  * <description>: resumo direto com o fato, o impacto a longo prazo e a citação da fonte dentro de uma tag <![CDATA[ ... ]]>.

Retorne APENAS o código XML puro, começando em <?xml version="1.0" encoding="UTF-8"?>.
Não inclua blocos markdown (como ```xml ou ```).
"""

# Executa com pesquisa do Google habilitada para buscar fatos reais das últimas 24h
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())]
    )
)

conteudo_xml = response.text.strip()

# Limpeza de eventuais delimitadores de código
if conteudo_xml.startswith("```xml"):
    conteudo_xml = conteudo_xml[6:]
if conteudo_xml.startswith("```"):
    conteudo_xml = conteudo_xml[3:]
if conteudo_xml.endswith("```"):
    conteudo_xml = conteudo_xml[:-3]

conteudo_xml = conteudo_xml.strip()

# Salva na raiz do repositório como feed.xml
with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(conteudo_xml)

print("feed.xml gerado e salvo com sucesso.")
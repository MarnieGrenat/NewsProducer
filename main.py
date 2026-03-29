import os
from dotenv import load_dotenv

from src.base_agent.gemini_agent import GeminiAgent
from src.writer.press_writer import Writer

from src.prompt_reader import PromptReader

# TODO
# Corrigir get_type (+ descritivo e ajustar para Prompt)
# Reorganizar prompt atual para fazer sentido com a classe (agent type)

ITERATIONS = 3

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("APIKEY is not set")

prompt = PromptReader("./config/prompts.json")

print("starting this sheet")

writer = Writer(
    llm=GeminiAgent(api_key=API_KEY, prompt=prompt.get_prompt("writer"), temperature=0.87),
    writer_type=prompt.get_type("writer")
)

critic = Writer(
    llm=GeminiAgent(api_key=API_KEY, prompt=prompt.get_prompt("critic"), temperature=0.9),
    writer_type=prompt.get_type("critic")
)

editor = Writer(
    llm=GeminiAgent(api_key=API_KEY, prompt=prompt.get_prompt("editor"), temperature=0.51),
    writer_type=prompt.get_type("editor")
)

curator = Writer(
    llm=GeminiAgent(api_key=API_KEY, prompt=prompt.get_prompt("curator"), temperature=0.2),
    writer_type=prompt.get_type("curator")
)

def generate_news(context: str = ""):
    news = writer.write(context)
    print("\n========= WRITER ========\n" + news)

    for i in range(ITERATIONS):
        critic_response = critic.write(news)
        print("\n========= CRITIC ========\n" + critic_response)

        if critic_response.upper() in ["OK", "[OK]"]: break

        news = editor.write("News:\n" + news + "\n\n Critic:\n" + critic_response)
        print("\n========= EDITOR ========\n" + news)

    curator_response = curator.write(news)
    print("\n========= CURATOR ========\n" + curator_response)


context = """
data de publicação: 2026-03-27
O empresário Luiz Rubini, ex-sócio do Grupo Fictor, figura entre os integrantes do Conselho do Desenvolvimento Econômico Social Sustentável (CDESS), órgão consultivo da Presidência da República conhecido como “Conselhão”. A informação foi publicada inicialmente pelo Estadão.
Rubini foi alvo de mandados de busca e apreensão nesta quarta-feira (25), no âmbito de uma operação da Polícia Federal que apura um amplo esquema de fraudes bancárias. Ele havia sido nomeado ao colegiado em agosto do ano passado, com mandato previsto até 2027, sob a justificativa de sua atuação em áreas como tecnologia, investimentos e agronegócio.
O Palácio do Planalto não comentou o caso até o momento. Já a defesa de Rubini afirmou, segundo o Estadão/Broadcast, que não teve conhecimento prévio das investigações e que deverá se manifestar em momento oportuno.
O chamado “Conselhão” é um grupo de caráter consultivo vinculado à Presidência da República, coordenado pela Secretaria de Relações Institucionais. Criado em 2003, no primeiro mandato do presidente Luiz Inácio Lula da Silva, o colegiado foi descontinuado durante o governo Jair Bolsonaro e posteriormente retomado.
Os conselheiros não recebem remuneração e têm como função contribuir com discussões estratégicas sobre políticas públicas. Em sua mais recente reformulação, realizada em 2025, o órgão passou a contar com cerca de 130 novos membros, oriundos de diferentes setores da sociedade.
Investigação aponta fraudes que podem ultrapassar R$ 500 milhões
A operação que mira Rubini também atingiu outros nomes ligados ao Grupo Fictor, incluindo o fundador e CEO da empresa, Rafael Góis. De acordo com informações reveladas primeiramente pelo Estadão, a investigação teve início em 2024 e identificou uma estrutura organizada voltada à prática de crimes financeiros.
Segundo a Polícia Federal, o grupo atuava por meio da criação de empresas de fachada e da cooptação de funcionários de instituições financeiras, facilitando a obtenção de crédito de forma fraudulenta. Há ainda indícios de conexão com organizações criminosas, incluindo ramificações associadas ao Comando Vermelho.
O esquema envolveria a criação em série de pessoas jurídicas com características padronizadas — como capital social fictício e objeto social genérico — utilizadas para viabilizar operações ilícitas no sistema financeiro.
No total, estão sendo cumpridos 43 mandados de busca e apreensão e 21 de prisão preventiva em cidades de São Paulo, Rio de Janeiro e Bahia. A Justiça também determinou o bloqueio de bens e ativos financeiros que podem chegar a R$ 47 milhões.
CVM também apura atuação da Fictor
Além da frente criminal, a Fictor também está sob investigação da Comissão de Valores Mobiliários (CVM) por suposta oferta irregular de investimentos. De acordo com o Estadão, a empresa teria divulgado aplicações financeiras sem a devida autorização do órgão regulador.
Recentemente, o grupo entrou com pedido de recuperação judicial, semanas após se envolver em uma operação relacionada ao Banco Master. O controlador da instituição, Daniel Vorcaro, encontra-se preso e negocia um acordo de delação premiada.
"""
generate_news(context)
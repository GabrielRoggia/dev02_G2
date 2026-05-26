"""
Script para gerar PDFs de regulamento esportivo de exemplo.
Execute uma vez para popular a pasta documentos/ antes de rodar a indexação.

    python gerar_documentos.py
"""
from fpdf import FPDF


def _sanitize(text: str) -> str:
    replacements = {
        "—": "-",  # em dash
        "–": "-",  # en dash
        "‘": "'",
        "’": "'",
        "“": '"',
        "”": '"',
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text


def criar_pdf(caminho: str, titulo: str, secoes: list[tuple[str, str]]):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, _sanitize(titulo), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(6)
    for subtitulo, conteudo in secoes:
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 9, _sanitize(subtitulo), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, _sanitize(conteudo))
        pdf.ln(4)
    pdf.output(caminho)
    print(f"PDF gerado: {caminho}")


REGULAMENTO_FUTEBOL = [
    (
        "Regra 1 - O Campo de Jogo",
        "O campo de futebol deve ser retangular, com comprimento entre 90 e 120 metros "
        "e largura entre 45 e 90 metros para partidas nacionais. Para partidas internacionais, "
        "o comprimento deve estar entre 100 e 110 metros e a largura entre 64 e 75 metros.\n\n"
        "A superfície do campo deve ser de relva natural ou artificial de cor verde. "
        "O campo é delimitado por linhas que fazem parte da área que definem. "
        "As duas linhas compridas de limite do campo são denominadas linhas laterais. "
        "As duas linhas curtas são denominadas linhas de gol.\n\n"
        "A área de gol: em cada extremidade do campo, são traçadas duas linhas perpendiculares "
        "à linha de gol, a 5,5 metros de cada poste. Essas linhas estendem-se 5,5 metros para "
        "dentro do campo e são unidas por uma linha paralela à linha de gol.\n\n"
        "A área penal: em cada extremidade do campo, são traçadas duas linhas perpendiculares "
        "à linha de gol, a 16,5 metros de cada poste. Essas linhas estendem-se 16,5 metros "
        "para dentro do campo e são unidas por uma linha paralela à linha de gol.\n\n"
        "A marca penal (pênalti) fica a 11 metros do ponto central entre os postes.",
    ),
    (
        "Regra 2 - A Bola",
        "A bola deve ser esférica, de couro ou outro material adequado. "
        "A circunferência deve ser de no mínimo 68 cm e no máximo 70 cm. "
        "O peso deve ser de no mínimo 410 g e no máximo 450 g no início da partida. "
        "A pressão de ar deve ser entre 0,6 e 1,1 atmosfera (600 a 1100 g/cm²) ao nível do mar.\n\n"
        "Se a bola se partir ou se estragar durante a partida, o jogo é interrompido e reiniciado "
        "com uma bola ao chão no local onde a bola original ficou inutilizada. "
        "Se isso ocorrer durante uma cobrança de falta, pênalti, escanteio, tiro de meta ou "
        "lançamento lateral, o jogo é reiniciado da mesma forma.",
    ),
    (
        "Regra 3 - Número de Jogadores",
        "Uma partida é disputada por duas equipes, cada uma com no máximo onze jogadores, "
        "sendo um deles o goleiro. Uma partida não pode começar se uma das equipes tiver "
        "menos de sete jogadores.\n\n"
        "Substituições: Em competições organizadas pela FIFA, cada equipe pode realizar "
        "até 5 substituições por partida, podendo ser feitas em até 3 momentos durante "
        "o tempo regulamentar, mais uma oportunidade adicional durante a prorrogação. "
        "O goleiro pode ser substituído por qualquer outro jogador da equipe.\n\n"
        "Se um goleiro fica impossibilitado de continuar e todas as substituições foram "
        "realizadas, qualquer jogador de linha pode assumir a posição de goleiro. "
        "Cada equipe deve designar um goleiro, identificado pela cor de sua camisa.",
    ),
    (
        "Regra 4 - Equipamento dos Jogadores",
        "O equipamento obrigatório de um jogador consiste em: camisa ou camiseta com mangas, "
        "calção, meias, protetor de canela e calçado.\n\n"
        "Os protetores de canela devem ser completamente cobertos pelas meias e feitos de "
        "material adequado (borracha, plástico ou material similar) para oferecer proteção adequada.\n\n"
        "O goleiro deve usar cores que o diferenciem dos outros jogadores e dos árbitros. "
        "Cada goleiro deve usar uma camisa de cor diferente dos outros jogadores e árbitros.\n\n"
        "Um jogador não pode usar equipamento ou qualquer objeto que seja perigoso para "
        "si mesmo ou para outro jogador, incluindo qualquer tipo de joias.",
    ),
    (
        "Regra 5 - O Árbitro",
        "Cada partida é controlada por um árbitro que tem plena autoridade para fazer cumprir "
        "as Regras do Jogo em relação à partida para a qual foi designado.\n\n"
        "Poderes e deveres do árbitro: aplicar as Regras do Jogo; controlar a partida com "
        "os assistentes e, onde aplicável, o quarto árbitro; garantir que as bolas usadas "
        "cumpram os requisitos da Regra 2; garantir que o equipamento dos jogadores cumpra "
        "os requisitos da Regra 4; atuar como cronometrista e registrar a partida.\n\n"
        "O árbitro pode expulsar da área de jogo e das suas imediações qualquer oficial de "
        "equipe que não cumpra as suas responsabilidades. O árbitro tem a autoridade de "
        "suspender, interromper ou dar por encerrada a partida por qualquer infração das "
        "Regras ou por interferência exterior.",
    ),
    (
        "Regra 6 - Outros Oficiais de Jogo",
        "Dois assistentes do árbitro são designados para cada partida. Suas funções, sujeitas "
        "à decisão do árbitro, são indicar: quando a bola saiu completamente do campo; qual "
        "equipe tem direito ao escanteio, tiro de meta ou lançamento lateral; quando um "
        "jogador pode ser legalmente substituído; quando ocorre uma infração que o árbitro "
        "não pôde ver; quando infrações são cometidas próximas dos assistentes; quando um "
        "pênalti é cobrado, se o goleiro avança antes de a bola ser chutada e se a bola "
        "cruza a linha de gol.\n\n"
        "O quarto árbitro auxilia o árbitro principal, indica o tempo acrescido e controla "
        "as substituições durante a partida.",
    ),
]

REGRAS_JOGO = [
    (
        "Regra 7 - Duração da Partida",
        "A partida dura dois tempos iguais de 45 minutos cada, salvo acordo em contrário "
        "entre o árbitro e as duas equipes antes do início da partida. Qualquer acordo para "
        "alterar os períodos de jogo (por exemplo, reduzir cada período para 40 minutos "
        "por causa de falta de luz) deve ser feito antes do início da partida.\n\n"
        "Intervalo entre os dois tempos: os jogadores têm direito a um intervalo no "
        "meio do jogo que não deve exceder 15 minutos. As regras da competição devem "
        "indicar a duração do intervalo.\n\n"
        "Tempo acrescido: o árbitro acrescenta, em cada um dos períodos, o tempo perdido "
        "por substituições, avaliação e/ou remoção de jogadores lesionados, perda de tempo, "
        "sanções disciplinares, interrupções por VAR e qualquer outra causa.",
    ),
    (
        "Regra 8 - Início e Reinício da Partida",
        "Um sorteio decide que equipe começa com a bola e a equipe que vence escolhe "
        "qual baliza vai atacar no primeiro tempo. A equipe que vence o sorteio realiza "
        "o pontapé inicial para começar a partida ou, se aplicável, para reiniciá-la "
        "após o intervalo do segundo tempo ou das prorrogações.\n\n"
        "Pontapé de saída: o árbitro dá o sinal para que a partida comece; a bola "
        "deve ser colocada no círculo central; todos os jogadores devem estar na "
        "sua metade do campo; os adversários da equipe que vai realizar o pontapé "
        "de saída devem estar fora do círculo central, a pelo menos 9,15 metros da bola.\n\n"
        "Bola ao chão: o jogo é reiniciado com uma bola ao chão para o goleiro da "
        "equipe que estava na posse da bola, ou para o jogador que estava com a bola "
        "na mão (para os goleiros) quando o jogo foi interrompido.",
    ),
    (
        "Regra 9 - Bola em Jogo e Fora do Jogo",
        "A bola está fora de jogo quando: ultrapassou completamente a linha lateral "
        "ou a linha de gol, tanto pelo chão como pelo ar; o jogo foi interrompido "
        "pelo árbitro.\n\n"
        "A bola está em jogo em todos os outros momentos, incluindo quando: ricocheta "
        "num poste, travessão ou bandeira de canto e permanece em campo; ricocheta "
        "no árbitro ou num assistente do árbitro quando eles estão em campo.",
    ),
    (
        "Regra 10 - Gol Marcado",
        "Um gol é marcado quando a bola cruza completamente a linha de gol entre "
        "os postes e por baixo da travessão, desde que nenhuma infração das Regras "
        "do Jogo tenha sido cometida pela equipe que marcou.\n\n"
        "Gols com a mão/braço: um gol não é válido se a bola tocou a mão ou o "
        "braço de um jogador atacante (incluindo o goleiro), seja intencional ou "
        "não, imediatamente antes de entrar no gol. Um gol marcado pelo goleiro "
        "diretamente com a mão ou braço é inválido, exceto em situações específicas.\n\n"
        "A equipe que marcar mais gols durante uma partida vence. Se ambas as "
        "equipes marcarem o mesmo número de gols ou nenhum gol for marcado, "
        "a partida termina empatada.",
    ),
    (
        "Regra 11 - Impedimento (Offside)",
        "Uma posição de impedimento não é uma infração por si só. Um jogador está "
        "em posição de impedimento se qualquer parte de sua cabeça, corpo ou pernas "
        "estiver na metade do campo dos adversários (excluindo a linha de meio-campo) "
        "e mais próxima da linha de gol dos adversários do que a bola e o penúltimo adversário.\n\n"
        "Um jogador não está em posição de impedimento se estiver alinhado com o "
        "penúltimo adversário ou com os dois últimos adversários.\n\n"
        "Uma infração de impedimento é cometida se um jogador em posição de "
        "impedimento no momento em que a bola é tocada ou jogada por um companheiro "
        "de equipe se envolver no jogo ativo: interferindo no jogo, interferindo com "
        "um adversário, ou ganhando uma vantagem ao estar nessa posição.",
    ),
    (
        "Regra 12 - Faltas e Incorreções",
        "Infrações punidas com pontapé livre direto: cometer uma falta de carga, "
        "saltar sobre, chutar ou tentar chutar, empurrar, atingir ou tentar atingir, "
        "atacar, disputar a bola com falta por deslizamento um adversário de forma "
        "considerada pelo árbitro como imprudente, com força excessiva ou violência.\n\n"
        "Cartão amarelo: é mostrado a um jogador que comete as seguintes infrações: "
        "retardamento na retomada do jogo, discordância com palavras ou ações com "
        "decisões do árbitro, entrar ou sair do campo sem permissão, infringir o "
        "Código de Conduta, simulação de falta ou lesão.\n\n"
        "Cartão vermelho: é mostrado a um jogador que comete as seguintes infrações: "
        "falta grave, conduta violenta, cuspir sobre alguém, impedir um gol ou uma "
        "clara oportunidade de gol através de uma falta punível com tiro livre ou "
        "pênalti, uso de linguagem ou gestos ofensivos, insultuosos ou abusivos, "
        "receber um segundo cartão amarelo na mesma partida.",
    ),
    (
        "Regra 13 - Pontapés Livres",
        "Os pontapés livres são diretos ou indiretos. Tanto o pontapé livre direto "
        "como o indireto devem ser cobrados com a bola em repouso e o cobrador não "
        "pode tocar na bola novamente antes de ela ser tocada por outro jogador.\n\n"
        "Pontapé livre direto: se um pontapé livre direto for cobrado diretamente "
        "para dentro da baliza adversária, um gol é concedido.\n\n"
        "Pontapé livre indireto: o árbitro indica o pontapé livre indireto levantando "
        "a mão acima da cabeça. Ele mantém a mão nessa posição até que o pontapé "
        "seja cobrado e a bola toque em outro jogador ou saia de jogo. Um gol pode "
        "ser marcado somente se a bola tocar em outro jogador antes de entrar na baliza.",
    ),
    (
        "Regra 14 - O Pontapé de Pênalti",
        "Um pontapé de pênalti é concedido quando um jogador comete uma das infrações "
        "puníveis com um pontapé livre direto dentro da própria área de penalidade e "
        "enquanto a bola está em jogo.\n\n"
        "Procedimento: a bola é colocada na marca de pênalti; o jogador que vai cobrar "
        "o pênalti é identificado; o goleiro defensor deve permanecer na linha de gol, "
        "entre os postes, de frente para o cobrador, até a bola ser chutada; os outros "
        "jogadores devem estar dentro do campo, fora da área de penalidade, atrás da "
        "marca de pênalti e a pelo menos 9,15 metros desta.\n\n"
        "O cobrador chuta a bola para frente. A bola está em jogo quando é chutada "
        "e claramente em movimento. O cobrador não pode tocar na bola novamente até "
        "que ela toque em outro jogador.",
    ),
    (
        "Regra 15 - O Lançamento Lateral",
        "O lançamento lateral é um método de reinício do jogo. Um gol não pode ser "
        "marcado diretamente a partir de um lançamento lateral. O lançamento lateral "
        "é concedido quando a bola cruza completamente a linha lateral, tanto pelo "
        "chão como pelo ar.\n\n"
        "Procedimento: o lançamento lateral deve ser realizado do local onde a bola "
        "cruzou a linha lateral; deve ser realizado por um jogador da equipe adversária "
        "à do jogador que tocou por último na bola; o executor deve, ao lançar a bola, "
        "estar de frente para o campo e ter parte de cada pé na linha lateral ou fora "
        "do campo; segurar a bola com as duas mãos e lançá-la de cima da cabeça.",
    ),
    (
        "Regra 16 - O Tiro de Meta",
        "O tiro de meta é um método de reinício do jogo. Um gol pode ser marcado "
        "diretamente a partir de um tiro de meta, mas somente contra a equipe adversária. "
        "O tiro de meta é concedido quando a bola cruza completamente a linha de gol, "
        "tanto pelo chão como pelo ar, sem que tenha entrado na baliza, e o último "
        "jogador a tocar na bola tenha sido um jogador da equipe atacante.\n\n"
        "Procedimento: a bola deve ser colocada em qualquer ponto dentro da área de gol "
        "pelo goleiro; os adversários devem ficar fora da área de penalidade até a bola "
        "estar em jogo; a bola está em jogo quando é chutada diretamente para fora da "
        "área de penalidade.",
    ),
    (
        "Regra 17 - O Pontapé de Canto (Escanteio)",
        "O escanteio é um método de reinício do jogo. Um gol pode ser marcado "
        "diretamente a partir de um escanteio, mas somente contra a equipe adversária. "
        "O escanteio é concedido quando a bola cruza completamente a linha de gol, "
        "tanto pelo chão como pelo ar, sem que tenha entrado na baliza, e o último "
        "jogador a tocar na bola tenha sido um jogador da equipe defensora.\n\n"
        "Procedimento: a bola é colocada dentro do arco de canto mais próximo do "
        "ponto onde a bola saiu; a bandeirinha do canto não pode ser movida; os "
        "adversários devem ficar a pelo menos 9,15 metros do arco de canto até a "
        "bola estar em jogo; a bola é cobrada por um jogador da equipe atacante; "
        "a bola está em jogo quando é chutada e claramente em movimento.",
    ),
]


if __name__ == "__main__":
    criar_pdf(
        "documentos/regulamento_futebol_parte1.pdf",
        "Regulamento de Futebol — Regras do Jogo (Parte 1)",
        REGULAMENTO_FUTEBOL,
    )
    criar_pdf(
        "documentos/regulamento_futebol_parte2.pdf",
        "Regulamento de Futebol — Regras do Jogo (Parte 2)",
        REGRAS_JOGO,
    )
    print("\nDocumentos gerados com sucesso em documentos/")
    print("Agora rode: python src/ingestao.py")

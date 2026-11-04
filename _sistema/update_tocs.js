const fs = require('fs');
const path = require('path');

const dataFile = path.join(__dirname, 'biblioteca_data', 'livros_data.js');
const content = fs.readFileSync(dataFile, 'utf8');
const window = {};
eval(content);
const books = window.BIBLIOTECA_LIVROS;

const tocs = {
  antimedo_versa_o_2_0: [
    { id: 'h_antimedo_0', lvl: 1, page: 5, title: 'Sumário' },
    { id: 'h_antimedo_1', lvl: 1, page: 7, title: '1. Seu maior bloqueio tem intimidade com o seu propósito' },
    { id: 'h_antimedo_2', lvl: 1, page: 13, title: '2. Você é o que você pensa' },
    { id: 'h_antimedo_3', lvl: 1, page: 23, title: '3. Medo X Medo' },
    { id: 'h_antimedo_4', lvl: 1, page: 29, title: '4. Estágios cerebrais do medo' },
    { id: 'h_antimedo_5', lvl: 1, page: 35, title: '5. Quais são os seus medos?' },
    { id: 'h_antimedo_6', lvl: 1, page: 39, title: '6. Sinal X Ruído' },
    { id: 'h_antimedo_7', lvl: 1, page: 45, title: '7. O preço da inércia' },
    { id: 'h_antimedo_8', lvl: 1, page: 49, title: '8. O ciclo do medo' },
    { id: 'h_antimedo_9', lvl: 1, page: 53, title: '9. Alienação' },
    { id: 'h_antimedo_10', lvl: 1, page: 59, title: '10. Irmãs do medo' },
    { id: 'h_antimedo_11', lvl: 1, page: 63, title: '11. Crenças limitantes' },
    { id: 'h_antimedo_12', lvl: 1, page: 73, title: '12. Ame problemas' },
    { id: 'h_antimedo_13', lvl: 1, page: 79, title: '13. Autoimagem' },
    { id: 'h_antimedo_14', lvl: 1, page: 85, title: '14. Lutar ou Fugir' },
    { id: 'h_antimedo_15', lvl: 1, page: 91, title: '15. Controle mental absoluto' },
    { id: 'h_antimedo_16', lvl: 1, page: 95, title: '16. Modelagem Inspiradora' },
    { id: 'h_antimedo_17', lvl: 1, page: 99, title: '17. O verdadeiro amor derrota o medo' },
    { id: 'h_antimedo_18', lvl: 1, page: 105, title: '18. Estado desejado' },
    { id: 'h_antimedo_19', lvl: 1, page: 111, title: '19. Antimedo' },
    { id: 'h_antimedo_20', lvl: 1, page: 117, title: '20. Quem é Pablo Marçal?' }
  ],
  a_arte_da_guerra_sun_tzu: [
    { id: 'h_suntzu_0', lvl: 1, page: 4, title: 'Índice Geral' },
    { id: 'h_suntzu_1', lvl: 1, page: 5, title: 'O Mais Antigo Tratado Militar do Mundo' },
    { id: 'h_suntzu_2', lvl: 1, page: 7, title: 'Vida de Sun Tzu' },
    { id: 'h_suntzu_3', lvl: 1, page: 12, title: 'Capítulo I — Da Avaliação' },
    { id: 'h_suntzu_4', lvl: 1, page: 16, title: 'Capítulo II — Do Comando da Guerra' },
    { id: 'h_suntzu_5', lvl: 1, page: 19, title: 'Capítulo III — Da Arte de Vencer sem Desembainhar a Espada' },
    { id: 'h_suntzu_6', lvl: 1, page: 24, title: 'Capítulo IV — Da Arte de Manobrar as Tropas' },
    { id: 'h_suntzu_7', lvl: 1, page: 28, title: 'Capítulo V — Do Confronto Direto e Indireto' },
    { id: 'h_suntzu_8', lvl: 1, page: 31, title: 'Capítulo VI — Do Cheio e do Vazio' },
    { id: 'h_suntzu_9', lvl: 1, page: 37, title: 'Capítulo VII — Da Arte do Confronto' },
    { id: 'h_suntzu_10', lvl: 1, page: 42, title: 'Capítulo VIII — Da Arte das Mudanças' },
    { id: 'h_suntzu_11', lvl: 1, page: 48, title: 'Capítulo IX — Da Importância da Geografia' },
    { id: 'h_suntzu_12', lvl: 1, page: 55, title: 'Capítulo X — Da Topografia' },
    { id: 'h_suntzu_13', lvl: 1, page: 61, title: 'Capítulo XI — Dos Nove Tipos de Terrenos' },
    { id: 'h_suntzu_14', lvl: 1, page: 72, title: 'Capítulo XII — Da Pirotecnia' },
    { id: 'h_suntzu_15', lvl: 1, page: 75, title: 'Capítulo XIII — Da Arte de Semear a Discórdia' }
  ],
  comunicar_vender_e_negociar_com_pnl: [
    { id: 'h_rventura_0', lvl: 1, page: 24, title: 'Sumário' },
    { id: 'h_rventura_1', lvl: 1, page: 25, title: 'A Quem se Destina Esse Livro?' },
    { id: 'h_rventura_2', lvl: 1, page: 27, title: 'Não sou vendedor, estou vendedor!' },
    { id: 'h_rventura_3', lvl: 1, page: 31, title: 'Manual de Instruções' },
    { id: 'h_rventura_4', lvl: 1, page: 33, title: 'PNL e Conceitos de Aprendizagem' },
    { id: 'h_rventura_5', lvl: 1, page: 35, title: 'História da PNL' },
    { id: 'h_rventura_6', lvl: 1, page: 39, title: 'Pressupostos Básicos da PNL' },
    { id: 'h_rventura_7', lvl: 1, page: 43, title: 'Como o Cérebro Processa Informações' },
    { id: 'h_rventura_8', lvl: 1, page: 51, title: 'Crenças Limitantes e Possibilitadoras' },
    { id: 'h_rventura_9', lvl: 1, page: 58, title: 'Filosofia do Sucesso' },
    { id: 'h_rventura_10', lvl: 1, page: 69, title: 'Mapas e Filtros' },
    { id: 'h_rventura_11', lvl: 1, page: 79, title: 'Rapport' },
    { id: 'h_rventura_12', lvl: 1, page: 99, title: 'Sistemas Representacionais' },
    { id: 'h_rventura_13', lvl: 1, page: 109, title: 'Critérios' },
    { id: 'h_rventura_14', lvl: 1, page: 121, title: 'Vamos Vender!' },
    { id: 'h_rventura_15', lvl: 1, page: 123, title: 'Técnica dos 101%' },
    { id: 'h_rventura_16', lvl: 1, page: 127, title: 'Técnica do Múltiplo Sim' },
    { id: 'h_rventura_17', lvl: 1, page: 133, title: 'Acordo Condicional' },
    { id: 'h_rventura_18', lvl: 1, page: 137, title: 'Informação Gratuita' },
    { id: 'h_rventura_19', lvl: 1, page: 141, title: 'A Palavra Não' },
    { id: 'h_rventura_20', lvl: 1, page: 145, title: 'A Palavra Mas' },
    { id: 'h_rventura_21', lvl: 1, page: 149, title: 'Pressuposições' },
    { id: 'h_rventura_22', lvl: 1, page: 153, title: 'Pistas Não Verbais' },
    { id: 'h_rventura_23', lvl: 1, page: 161, title: 'Estratégia para Negociação' },
    { id: 'h_rventura_24', lvl: 1, page: 169, title: 'Formatando Reuniões' },
    { id: 'h_rventura_25', lvl: 1, page: 175, title: 'Administração do Tempo' },
    { id: 'h_rventura_26', lvl: 1, page: 179, title: 'O Presente Precioso' },
    { id: 'h_rventura_27', lvl: 1, page: 189, title: 'Metamodelo e Metaprograma' },
    { id: 'h_rventura_28', lvl: 1, page: 197, title: 'Metaprogramas em Vendas e Negociação' },
    { id: 'h_rventura_29', lvl: 1, page: 217, title: 'Um Pouco de C.G. Jung' },
    { id: 'h_rventura_30', lvl: 1, page: 221, title: 'Final e Bibliografia' }
  ],
  introdu_o_a_pnl_joseph_o_connor: [
    { id: 'h_oconnor_0', lvl: 1, page: 5, title: 'Índice Analítico' },
    { id: 'h_oconnor_1', lvl: 1, page: 9, title: 'Apresentação (Robert B. Dilts)' },
    { id: 'h_oconnor_2', lvl: 1, page: 10, title: 'Prefácio (John Grinder)' },
    { id: 'h_oconnor_3', lvl: 1, page: 11, title: 'Introdução' },
    { id: 'h_oconnor_4', lvl: 1, page: 13, title: 'Agradecimentos' },
    { id: 'h_oconnor_5', lvl: 1, page: 16, title: 'Capítulo 1 — O que é Programação Neurolingüística?' },
    { id: 'h_oconnor_6', lvl: 1, page: 39, title: 'Capítulo 2 — As Portas da Percepção' },
    { id: 'h_oconnor_7', lvl: 1, page: 59, title: 'Capítulo 3 — O Estado de Espírito e Recursos' },
    { id: 'h_oconnor_8', lvl: 1, page: 79, title: 'Capítulo 4 — Sistemas: Corpos e Mentes' },
    { id: 'h_oconnor_9', lvl: 1, page: 99, title: 'Capítulo 5 — Palavras e Significados' },
    { id: 'h_oconnor_10', lvl: 1, page: 122, title: 'Capítulo 6 — Além das Palavras: Linguagem Não-Verbal' },
    { id: 'h_oconnor_11', lvl: 1, page: 151, title: 'Capítulo 7 — Padrões de PNL nos Negócios' },
    { id: 'h_oconnor_12', lvl: 1, page: 178, title: 'Capítulo 8 — Terapia e Mudança Pessoal' },
    { id: 'h_oconnor_13', lvl: 1, page: 188, title: 'Capítulo 9 — Estratégias Mentais e Modelagem' },
    { id: 'h_oconnor_14', lvl: 1, page: 216, title: 'Epílogo: Investindo em Si Mesmo' },
    { id: 'h_oconnor_15', lvl: 1, page: 221, title: 'Glossário' }
  ]
};

Object.keys(tocs).forEach(bookId => {
  const b = books.find(x => x.id === bookId);
  if (!b) return;
  const items = tocs[bookId];
  b.toc = items;
  
  // Insert headings into content
  items.forEach(item => {
    const exists = b.content.find(c => c.id === item.id);
    if (!exists) {
      let targetIdx = b.content.findIndex(c => c.page >= item.page);
      if (targetIdx === -1) targetIdx = b.content.length;
      b.content.splice(targetIdx, 0, {
        type: 'heading',
        id: item.id,
        lvl: item.lvl,
        title: item.title,
        page: item.page
      });
    }
  });
  console.log(`Updated ${b.id} with ${items.length} TOC items.`);
});

fs.writeFileSync(dataFile, 'window.BIBLIOTECA_LIVROS = ' + JSON.stringify(books, null, 2) + ';\n', 'utf8');
console.log('Successfully wrote updated livros_data.js!');


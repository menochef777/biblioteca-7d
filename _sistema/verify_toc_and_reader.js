const fs = require('fs');
const path = require('path');
const vm = require('vm');

console.log('--- TESTE COMPLETO DO SUMÁRIO E LEITOR ---');

// 1. Carregar dados dos livros
const dataCode = fs.readFileSync(path.join(__dirname, 'biblioteca_data', 'livros_data.js'), 'utf8');
const context = {
  window: {},
  document: {
    getElementById: () => null,
    querySelectorAll: () => [],
    createElement: () => ({ style: {}, appendChild: () => {}, setAttribute: () => {} })
  },
  localStorage: {
    getItem: () => null,
    setItem: () => {}
  },
  console: console
};
vm.createContext(context);
vm.runInContext(dataCode, context);

const books = context.window.BIBLIOTECA_LIVROS;
console.log(`Carregados ${books.length} livros.`);

let totalTOCItems = 0;
let errors = [];

books.forEach((b, idx) => {
  if (!b.toc || b.toc.length === 0) {
    errors.push(`Livro ${b.id} não possui itens no sumário!`);
  } else {
    totalTOCItems += b.toc.length;
    // Verificar cada item
    const contentIds = new Set(b.content.map(c => c.id).filter(Boolean));
    const contentPages = new Set(b.content.map(c => c.page).filter(Boolean));

    b.toc.forEach(item => {
      if (!item.title) errors.push(`${b.id}: item sem título: ${JSON.stringify(item)}`);
      const hasId = contentIds.has(item.id);
      const hasPage = contentPages.has(item.page);
      if (!hasId && !hasPage) {
        errors.push(`${b.id}: TOC item "${item.title}" nem ID nem Página encontrada!`);
      }
    });
  }
});

console.log(`Total de itens de sumário nos 14 livros: ${totalTOCItems}`);
if (errors.length > 0) {
  console.error('ERROS ENCONTRADOS:', errors);
  process.exit(1);
} else {
  console.log('✅ 100% DOS 14 LIVROS COM SUMÁRIOS VÁLIDOS E FUNCIONAIS!');
}

// 2. Validar sintaxe JS de index.html
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const scriptMatches = html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi);
let scriptIdx = 0;
for (const match of scriptMatches) {
  scriptIdx++;
  const scriptContent = match[1];
  if (!match[0].includes('src=')) {
    try {
      new vm.Script(scriptContent);
      console.log(`✅ Script inline #${scriptIdx} sintaxe 100% válida.`);
    } catch (err) {
      console.error(`❌ Erro no script inline #${scriptIdx}:`, err.message);
      process.exit(1);
    }
  }
}

console.log('🎉 TUDO PRONTO E VALIDADO COM SUCESSO!');

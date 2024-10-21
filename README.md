## Chat Application
Este repositório contém um aplicativo de chat desenvolvido com Next.js, React e TypeScript. O objetivo do projeto é fornecer uma interface de chat onde os usuários podem interagir com um assistente virtual, realizar login e gerenciar suas contas.

## Estrutura do Projeto
O projeto é organizado nas seguintes pastas e arquivos principais:

src/app/(chat)/layout.tsx: Componente de layout que envolve a estrutura do chat, incluindo o cabeçalho e a área principal do chat.

src/app/(chat)/page.tsx: Página principal do chat que verifica a autenticação do usuário e renderiza o componente de chat.

src/app/auth/layout.tsx: Componente de layout para as páginas de autenticação.

src/app/auth/page.tsx: Página de login, onde os usuários podem inserir suas credenciais. A validação é feita utilizando Formik e Yup.

src/app/layout.tsx: Layout raiz do aplicativo, onde são definidas as fontes e metadados.

src/components/button.tsx: Componente de botão reutilizável.

src/components/chat.tsx: Componente do chat que gerencia as mensagens enviadas e recebidas.

src/components/header.tsx: Cabeçalho do aplicativo que inclui um botão de logout.

src/components/inputField.tsx: Componente de campo de entrada reutilizável para formulários.

src/components/modalAuth.tsx: Modal de autenticação que contém os formulários de login e registro.

src/components/textBar.tsx: Componente da barra de texto para enviar mensagens.

## Instruções de Uso
### Clone o repositório:
git clone <URL do repositório>
cd <nome do repositório>


### Instale as dependências:
npm install

### Inicie o servidor de desenvolvimento:
npm run dev
Acesse a aplicação: Abra o navegador e vá para http://localhost:3000.

## Funcionalidades
Autenticação: Os usuários podem realizar login e logout, utilizando um token armazenado no localStorage.
Chat em tempo real: Mensagens enviadas pelos usuários são processadas e respondidas pelo assistente virtual.
Validação de formulário: Utiliza Formik e Yup para validação de entradas de email e senha.

## Requisitos
Node.js
Um backend em execução em http://localhost:8000 para autenticação e envio de mensagens.
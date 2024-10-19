import { WebSocketServer } from 'ws';
import { NextApiRequest, NextApiResponse } from 'next';
import http from 'http';

let wss: WebSocketServer | null = null;

// Essa função vai iniciar o servidor WebSocket
export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (!wss) {
    const server = http.createServer((req, res) => res.end('WebSocket Server'));
    wss = new WebSocketServer({ server });

    wss.on('connection', (ws) => {
      ws.on('message', async (message: string) => {
        const content = JSON.parse(message).message;

        try {
          const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
              Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              model: 'gpt-4o',
              messages: [{ role: 'user', content }],
              stream: true, // Habilita o streaming
            }),
          });

          // Lê a resposta em chunks (partes)
          const reader = response.body?.getReader();
          const decoder = new TextDecoder('utf-8');
          let done = false;

          while (!done) {
            const { value, done: readerDone } = await reader!.read();
            done = readerDone;
            const chunk = decoder.decode(value, { stream: true });
            
            // Envia cada fragmento de resposta para o cliente WebSocket
            const lines = chunk.split('\n').filter(line => line.trim() !== '');
            for (const line of lines) {
              const json = line.replace(/^data: /, '');
              if (json === '[DONE]') {
                break;
              }
              const parsed = JSON.parse(json);
              const assistantMessage = parsed.choices[0]?.delta?.content;
              if (assistantMessage) {
                ws.send(JSON.stringify({ role: 'assistant', content: assistantMessage }));
              }
            }
          }
        } catch (error) {
          console.error('Erro ao processar a mensagem:', error);
          ws.send(JSON.stringify({ error: 'Erro ao processar a mensagem' }));
        }
      });
    });

    server.listen(4000, () => {
      console.log('WebSocket Server running on port 4000');
    });
  }

  res.status(200).json({ message: 'WebSocket server running' });
}

import re

with open('src/pages/Billing.tsx', 'r') as f:
    content = f.read()

webhook_info = """                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1">Nome da Instância</label>
                      <input
                        type="text"
                        placeholder="ex: WhatsAppPrincipal"
                        value={waSettings.evolutionInstanceName}
                        onChange={e => setWaSettings({...waSettings, evolutionInstanceName: e.target.value})}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary outline-none text-sm"
                      />
                    </div>
                    
                    <div className="col-span-1 md:col-span-3 mt-4 bg-blue-50 border border-blue-100 p-4 rounded-lg">
                      <h4 className="font-bold text-blue-800 flex items-center mb-2">
                        <MessageSquare size={16} className="mr-2" />
                        Configuração de Webhook (Para Receber Mensagens no Chat)
                      </h4>
                      <p className="text-sm text-blue-700 mb-2">
                        Para que as respostas dos seus clientes apareçam na janela de Chat do sistema, você precisa configurar um Webhook dentro da sua Evolution API.
                      </p>
                      <div className="bg-white p-3 rounded border border-blue-200">
                        <p className="text-xs font-semibold text-gray-500 mb-1">URL DO WEBHOOK:</p>
                        <code className="text-sm text-gray-800 break-all select-all">
                          https://ais-pre-lafhr3cxydhbm5z265hztr-86812857430.us-east1.run.app/api/webhook/evolution
                        </code>
                        <p className="text-xs text-gray-500 mt-2"><b>Eventos necessários:</b> messages-upsert</p>
                      </div>
                    </div>"""

content = re.sub(r"(                    <div>\n                      <label className=\"block text-xs font-medium text-gray-700 mb-1\">Nome da Instância</label>\n                      <input\n                        type=\"text\"\n                        placeholder=\"ex: WhatsAppPrincipal\"\n                        value=\{waSettings.evolutionInstanceName\}\n                        onChange=\{e => setWaSettings\(\{\.\.\.waSettings, evolutionInstanceName: e\.target\.value\}\)\}\n                        className=\"w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary outline-none text-sm\"\n                      />\n                    </div>)", webhook_info, content, count=1)

with open('src/pages/Billing.tsx', 'w') as f:
    f.write(content)

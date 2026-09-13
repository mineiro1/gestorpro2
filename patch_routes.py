import re

with open('src/pages/RoutesPage.tsx', 'r') as f:
    content = f.read()

old_code = """            let message = useMessage2 ? msg2 : msg1;
            message = message.replace(/{nome}/g, clientName).replace(/{telefone}/g, cleanPhone);
            
            if (waSettings.useSmsForReports) {"""

new_code = """            let message = useMessage2 ? msg2 : msg1;
            message = message.replace(/{nome}/g, clientName).replace(/{telefone}/g, cleanPhone);
            
            let currentSettings = waSettings;
            if (userProfile?.uid) {
              const { data } = await supabase.from('users').select('whatsapp_settings').eq('id', adminId).single();
              if (data && data.whatsapp_settings) {
                currentSettings = { ...waSettings, ...data.whatsapp_settings };
              }
            }

            if (currentSettings.useSmsForReports) {"""

content = content.replace(old_code, new_code)

with open('src/pages/RoutesPage.tsx', 'w') as f:
    f.write(content)

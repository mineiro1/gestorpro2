import re

with open('src/components/Layout.tsx', 'r') as f:
    content = f.read()

old_code = """    const handleNewVisit = (payload: any) => {
      if (payload.new) {
        const isAssignedToMe = payload.new.employee_id === userProfile.uid;
        const isAdminOwner = userProfile.role === 'admin' && payload.new.admin_id === userProfile.uid;

        if (isAssignedToMe || isAdminOwner) {
          const msg = isAssignedToMe 
            ? 'Você tem uma nova visita/manutenção agendada para hoje!'
            : 'Uma nova visita foi criada no sistema.';
          showNotification('Nova Visita Agendada', msg);
        }
      }
    };"""

new_code = """    const handleNewVisit = async (payload: any) => {
      if (payload.new) {
        const isAdminOwner = userProfile.role === 'admin' && payload.new.admin_id === userProfile.uid;
        // Don't notify the admin if they did it themselves (optional, but good UX)
        const isSelf = payload.new.employee_id === userProfile.uid;

        if (isAdminOwner && !isSelf) {
          try {
            const { data: empData } = await supabase.from('users').select('name').eq('id', payload.new.employee_id).single();
            const { data: cliData } = await supabase.from('clients').select('name').eq('id', payload.new.client_id).single();
            
            const empName = empData?.name || 'Colaborador';
            const cliName = cliData?.name || 'Cliente';
            
            showNotification('Visita Finalizada', `O colaborador ${empName} finalizou a visita no cliente ${cliName}.`);
          } catch (e) {
            showNotification('Visita Finalizada', 'Um colaborador finalizou uma visita.');
          }
        }
      }
    };"""

content = content.replace(old_code, new_code)

with open('src/components/Layout.tsx', 'w') as f:
    f.write(content)

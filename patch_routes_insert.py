import re

with open('src/pages/RoutesPage.tsx', 'r') as f:
    content = f.read()

insert_regex = re.compile(r"            const \{ error: insertError \} = await supabase\.from\('visits'\)\.insert\(\{\n              admin_id: adminId,\n              client_id: selectedClientForReport\.id,\n              employee_id: payload\.employeeId,\n              date: finalVisitDate,\n              time: activeRouteDate,\n              notes: finalNotes,\n              photo_urls: reportPhotos,\n              location: locationData\n            \}\);")

new_logic = """
            // Check if there's an 'agendada' visit for today
            const { data: existingAgendada } = await supabase.from('visits')
              .select('id')
              .eq('client_id', selectedClientForReport.id)
              .eq('date', routeDate) // this was used to insert the agendada
              .limit(1);

            let insertError = null;
            if (existingAgendada && existingAgendada.length > 0) {
              const { error } = await supabase.from('visits').update({
                date: finalVisitDate,
                time: activeRouteDate,
                notes: finalNotes,
                photo_urls: reportPhotos,
                location: locationData,
                status: 'finalizada'
              }).eq('id', existingAgendada[0].id);
              insertError = error;
            } else {
              const { error } = await supabase.from('visits').insert({
                admin_id: adminId,
                client_id: selectedClientForReport.id,
                employee_id: payload.employeeId,
                date: finalVisitDate,
                time: activeRouteDate,
                notes: finalNotes,
                photo_urls: reportPhotos,
                location: locationData,
                status: 'finalizada'
              });
              insertError = error;
            }
"""

content = insert_regex.sub(new_logic, content)

with open('src/pages/RoutesPage.tsx', 'w') as f:
    f.write(content)

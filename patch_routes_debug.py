import re

with open('src/pages/RoutesPage.tsx', 'r') as f:
    content = f.read()

debug_log = """
      if (existingVisit && existingVisit.length > 0) {
         visitId = existingVisit[0].id;
         console.log("Found existing visit:", visitId);
      } else {
         const { data: newVisit, error: newVisitErr } = await supabase.from('visits').insert({
           admin_id: adminId,
           client_id: client.id,
           employee_id: selectedEmployee || userProfile.uid,
           date: routeDate,
           status: 'agendada'
         }).select('id').single();
         console.log("Created new visit:", newVisit, "Err:", newVisitErr);
         if (newVisit) visitId = newVisit.id;
      }
"""

content = re.sub(r"(      if \(existingVisit && existingVisit\.length > 0\) \{[\s\S]*?if \(newVisit\) visitId = newVisit\.id;\n      \})", debug_log, content, count=1)

with open('src/pages/RoutesPage.tsx', 'w') as f:
    f.write(content)

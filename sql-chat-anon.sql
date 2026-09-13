create policy "Allow anon inserts for backend" on chat_messages for insert to anon with check (true);
create policy "Allow anon selects for backend" on clients for select to anon using (true);
create policy "Allow anon selects for backend" on chat_sessions for select to anon using (true);
create policy "Allow anon updates for backend" on chat_sessions for update to anon using (true) with check (true);

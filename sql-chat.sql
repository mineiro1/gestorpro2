-- 1. Adicionar telefone local ao cliente
alter table clients add column if not exists local_phone text;

-- 2. Criar tabela de sessões de chat
create table if not exists chat_sessions (
  id uuid default uuid_generate_v4() primary key,
  visit_id uuid references visits(id),
  admin_id uuid references users(id) not null,
  client_id uuid references clients(id) not null,
  employee_id uuid references users(id) not null,
  status text default 'open',
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  closed_at timestamp with time zone
);
alter table chat_sessions enable row level security;
create policy "Allow all operations for authenticated users on chat_sessions" on chat_sessions for all to authenticated using (true) with check (true);

-- 3. Criar tabela de mensagens
create table if not exists chat_messages (
  id uuid default uuid_generate_v4() primary key,
  session_id uuid references chat_sessions(id) not null,
  sender_type text not null check (sender_type in ('tech', 'client')),
  content text,
  media_url text,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);
alter table chat_messages enable row level security;
create policy "Allow all operations for authenticated users on chat_messages" on chat_messages for all to authenticated using (true) with check (true);

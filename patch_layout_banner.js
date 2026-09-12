const fs = require('fs');
let content = fs.readFileSync('src/components/Layout.tsx', 'utf8');

// import Bell icon
if (!content.includes('Bell')) {
  content = content.replace(/import \{([^}]+)\} from 'lucide-react';/, "import { $1, Bell } from 'lucide-react';");
}

const bannerComponent = `
const NotificationBanner = () => {
  const [permission, setPermission] = useState(Notification.permission);
  const [dismissed, setDismissed] = useState(sessionStorage.getItem('notif_banner_dismissed') === 'true');

  if (permission !== 'default' || dismissed) return null;

  const requestPermission = async () => {
    try {
      let perm;
      if (Capacitor.isNativePlatform()) {
        const res = await LocalNotifications.requestPermissions();
        perm = res.display === 'granted' ? 'granted' : 'denied';
      } else {
        perm = await Notification.requestPermission();
        if (perm === 'granted' && 'serviceWorker' in navigator) {
           const reg = await navigator.serviceWorker.ready;
           // Explicitly show a welcome notification to confirm it works via SW
           reg.showNotification('Notificações Ativadas!', {
             body: 'Você receberá alertas de visitas finalizadas aqui.',
             icon: 'https://cdn-icons-png.flaticon.com/512/123/123382.png'
           });
        }
      }
      setPermission(perm);
    } catch (e) {
      console.error(e);
    }
  };

  const dismiss = () => {
    sessionStorage.setItem('notif_banner_dismissed', 'true');
    setDismissed(true);
  };

  return (
    <div className="bg-blue-600 text-white p-4 flex flex-col sm:flex-row items-center justify-between shadow-md relative z-50">
      <div className="flex items-center space-x-3 mb-2 sm:mb-0">
        <Bell className="w-6 h-6 animate-pulse" />
        <span className="text-sm font-medium">Ative as notificações para receber alertas quando um técnico finalizar uma visita.</span>
      </div>
      <div className="flex space-x-2">
        <button onClick={requestPermission} className="bg-white text-blue-600 px-4 py-1.5 rounded-md text-sm font-bold shadow hover:bg-blue-50 transition">Ativar</button>
        <button onClick={dismiss} className="bg-blue-700 text-white px-3 py-1.5 rounded-md text-sm hover:bg-blue-800 transition">Depois</button>
      </div>
    </div>
  );
};
`;

content = content.replace("export default function Layout() {", bannerComponent + "\nexport default function Layout() {");

const bannerInjection = `<NotificationBanner />
        <main className="flex-1 p-4`;

content = content.replace('<main className="flex-1 p-4', bannerInjection);

// Remove the auto-request permission that was failing or annoying
content = content.replace(/if \('Notification' in window && Notification\.permission === 'default'\) \{\s*Notification\.requestPermission\(\)\.catch\(\(\) => \{\}\);\s*\}/g, "");

fs.writeFileSync('src/components/Layout.tsx', content);

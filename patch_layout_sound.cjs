const fs = require('fs');
let content = fs.readFileSync('src/components/Layout.tsx', 'utf8');

// We need to modify showNotification to play the sound and add vibrate array
const regex = /const showNotification = async \(title: string, body: string\) => \{([\s\S]*?)new Notification\(title, \{ body, icon: 'https:\/\/cdn-icons-png\.flaticon\.com\/512\/123\/123382\.png' \}\);\s*\}\s*\}\s*\}\s*\};/m;

const replacement = `const showNotification = async (title: string, body: string) => {
      // Play custom sound
      try {
        const audio = new Audio('/notificacao.mp3');
        audio.play().catch(e => console.log("Audio play blocked by browser policy:", e));
      } catch (err) {
        console.error("Audio error", err);
      }

      if (Capacitor.isNativePlatform()) {
        try {
          await LocalNotifications.schedule({
            notifications: [
              {
                title,
                body,
                id: new Date().getTime(),
                schedule: { at: new Date(Date.now() + 1000) },
                sound: 'notificacao.mp3' // Attempt to use custom sound in Capacitor if configured, otherwise default
              }
            ]
          });
        } catch (e) {
          console.error("Capacitor local notification error", e);
        }
      } else {
        if ('Notification' in window && Notification.permission === 'granted') {
          if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
            navigator.serviceWorker.ready.then(registration => {
              registration.showNotification(title, {
                body,
                icon: 'https://cdn-icons-png.flaticon.com/512/123/123382.png',
                vibrate: [200, 100, 200, 100, 200], // Vibration pattern
              });
            });
          } else {
            new Notification(title, { 
              body, 
              icon: 'https://cdn-icons-png.flaticon.com/512/123/123382.png',
              vibrate: [200, 100, 200, 100, 200]
            });
          }
        }
      }
    };`;

content = content.replace(regex, replacement);

fs.writeFileSync('src/components/Layout.tsx', content);

// GMO Portal integration via iframe

export default function GMOPage() {
  return (
    <div style={{height: '100vh', width: '100vw', background: '#f9fafb'}}>
      <iframe
        src="http://localhost:8000"
        style={{ width: '100%', height: '100vh', border: 'none' }}
        title="GMO Portal"
        allowFullScreen
      />
    </div>
  );
} 
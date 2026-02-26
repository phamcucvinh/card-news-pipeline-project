import React from 'react';
import './App.css';

const App: React.FC = () => {
  const [content, setContent] = React.useState('');
  const currentDate = new Date().toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1 className="app-title">Minimal Diary</h1>
        </div>
        <nav className="sidebar-nav">
          <button className="nav-item active">📅 오늘</button>
          <button className="nav-item">📆 달력</button>
          <button className="nav-item">🔍 검색</button>
        </nav>
        <div className="sidebar-footer">
          <button className="nav-item">⚙️ 설정</button>
        </div>
      </aside>

      <main className="main-content">
        <div className="editor-container">
          <div className="editor-header">
            <p className="current-date">{currentDate}</p>
          </div>
          <textarea
            className="editor"
            placeholder="오늘 하루를 기록해보세요..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />
          <div className="editor-footer">
            <span className="word-count">{content.length} 글자</span>
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;

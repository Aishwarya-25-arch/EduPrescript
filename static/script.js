document.addEventListener('DOMContentLoaded', function() {
    const riskFilter = document.getElementById('riskFilter');
    const gradeFilter = document.getElementById('gradeFilter');
    const searchStudent = document.getElementById('searchStudent');

    if (riskFilter && gradeFilter && searchStudent) {
        filterStudents();

        riskFilter.addEventListener('change', filterStudents);
        gradeFilter.addEventListener('change', filterStudents);
        searchStudent.addEventListener('input', filterStudents);
    }

    const checkboxes = document.querySelectorAll('.checklist-item input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const item = this.closest('.checklist-item');
            if (this.checked) {
                item.classList.add('completed');
            } else {
                item.classList.remove('completed');
            }
            updateProgress();
        });
    });

    const addNoteForm = document.querySelector('.add-note-form');
    if (addNoteForm) {
        addNoteForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const textarea = this.querySelector('.note-textarea');
            const noteText = textarea.value.trim();

            if (noteText) {
                addNote(noteText);
                textarea.value = '';
            }
        });
    }
});

function filterStudents() {
    const riskFilter = document.getElementById('riskFilter').value;
    const gradeFilter = document.getElementById('gradeFilter').value;
    const searchTerm = document.getElementById('searchStudent').value.toLowerCase();

    const rows = document.querySelectorAll('.student-row');

    rows.forEach(row => {
        const risk = row.dataset.risk;
        const grade = row.dataset.grade;
        const name = row.querySelector('.student-name span').textContent.toLowerCase();

        let showRisk = riskFilter === 'all' || risk === riskFilter;
        let showGrade = gradeFilter === 'all' || grade === gradeFilter;
        let showSearch = searchTerm === '' || name.includes(searchTerm);

        if (showRisk && showGrade && showSearch) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

function updateProgress() {
    const allCheckboxes = document.querySelectorAll('.checklist-item input[type="checkbox"]');
    const checkedCheckboxes = document.querySelectorAll('.checklist-item input[type="checkbox"]:checked');

    const completed = checkedCheckboxes.length;
    const total = allCheckboxes.length;
    const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;

    const progressCircle = document.querySelector('.progress-circle circle:last-child');
    if (progressCircle) {
        const circumference = 314;
        const offset = circumference - (percentage / 100) * circumference;
        progressCircle.style.strokeDashoffset = offset;
    }

    const progressNumber = document.querySelector('.progress-number');
    if (progressNumber) {
        progressNumber.textContent = percentage + '%';
    }

    const completedStat = document.querySelector('.summary-stats .summary-stat:first-child h3');
    const remainingStat = document.querySelector('.summary-stats .summary-stat:nth-child(2) h3');

    if (completedStat) {
        completedStat.textContent = completed;
    }

    if (remainingStat) {
        remainingStat.textContent = total - completed;
    }
}

function addNote(noteText) {
    const notesList = document.querySelector('.notes-list');

    const noteItem = document.createElement('div');
    noteItem.className = 'note-item';

    const today = new Date();
    const dateStr = today.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

    noteItem.innerHTML = `
        <div class="note-meta">
            <span class="note-author">Current Teacher</span>
            <span class="note-date">${dateStr}</span>
        </div>
        <p>${noteText}</p>
    `;

    notesList.insertBefore(noteItem, notesList.firstChild);

    noteItem.style.opacity = '0';
    noteItem.style.transform = 'translateY(-10px)';
    noteItem.style.transition = 'all 0.3s ease';

    setTimeout(() => {
        noteItem.style.opacity = '1';
        noteItem.style.transform = 'translateY(0)';
    }, 10);
}

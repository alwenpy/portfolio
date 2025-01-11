function createNote(title, content) {
  return { title, content };
}

function readNote(note) {
  return note;
}

function updateNote(note, newTitle, newContent) {
  note.title = newTitle;
  note.content = newContent;
  return note;
}

function deleteNote(note) {
  return null; // or some indicator of deletion
}

const notes = [];

function displayNotes() {
  const dynamicSection = document.getElementById('dynamic');
  dynamicSection.innerHTML = ''; //clear previous notes
  const noteList = document.createElement('ul');
  noteList.style.listStyleType = 'none';
  noteList.style.padding = '0';

  notes.forEach(note => {
    const listItem = document.createElement('li');
    listItem.style.marginBottom = '10px';
    listItem.style.border = '1px solid #ccc';
    listItem.style.padding = '10px';
    listItem.style.borderRadius = '5px';

    const titleElement = document.createElement('h3');
    titleElement.textContent = note.title;
    listItem.appendChild(titleElement);

    const contentElement = document.createElement('p');
    contentElement.textContent = note.content;
    listItem.appendChild(contentElement);

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.style.backgroundColor = 'red';
    deleteButton.style.color = 'white';
    deleteButton.style.border = 'none';
    deleteButton.style.padding = '5px 10px';
    deleteButton.style.cursor = 'pointer';
    deleteButton.style.marginLeft = '10px';
    deleteButton.onclick = () => {
      const index = notes.indexOf(note);
      if (index > -1) {
        notes.splice(index, 1);
        displayNotes();
      }
    };
    listItem.appendChild(deleteButton);
    noteList.appendChild(listItem);

  });
  dynamicSection.appendChild(noteList);
}


//Example Usage
notes.push(createNote("Grocery List", "Milk, Eggs, Bread"));
notes.push(createNote("Meeting Notes", "Discuss project deadlines"));

displayNotes();


document.getElementById('addNote').addEventListener('click', () => {
    const newTitle = prompt("Enter note title:");
    const newContent = prompt("Enter note content:");
    if (newTitle && newContent) {
        notes.push(createNote(newTitle, newContent));
        displayNotes();
    }
});
async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        credentials: "same-origin",
        headers: {
            ...(options.headers || {}),
            ...(options.body ? { "Content-Type": "application/json" } : {})
        }
    });

    if (response.status === 401) {
        window.location.href = "/login.html";
        throw new Error("Необходимо войти в аккаунт");
    }

    if (!response.ok) {
        let message = "Произошла ошибка";

        try {
            const data = await response.json();
            message = Array.isArray(data.detail)
                ? data.detail.map(item => item.msg).join(", ")
                : data.detail || message;
        } catch {
        }

        throw new Error(message);
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
}

function showMessage(elementId, message, success = false) {
    const element = document.getElementById(elementId);

    if (!element) return;

    element.textContent = message;
    element.style.color = success ? "#287a48" : "#b52d4b";
}

function createElement(tag, className, text) {
    const element = document.createElement(tag);

    if (className) {
        element.className = className;
    }

    if (text !== undefined) {
        element.textContent = text;
    }

    return element;
}

function formatDate(value) {
    if (!value) return "Не указана";

    const parts = value.split("-");
    return parts.length === 3
        ? `${parts[2]}.${parts[1]}.${parts[0]}`
        : value;
}

let pets = [];
let recordTypes = [];

async function loadProfile() {
    const user = await apiRequest("/api/auth/me");

    const nameElement = document.getElementById("profile-name");
    const detailsElement = document.getElementById("profile-details");

    if (nameElement) {
        nameElement.textContent =
            `${user.first_name} ${user.last_name}`;
    }

    if (detailsElement) {
        detailsElement.textContent = user.username;
    }
}

async function loadPets() {
    const container = document.getElementById("pets-list");

    try {
        pets = await apiRequest("/api/pets/");

        container.replaceChildren();

        if (pets.length === 0) {
            container.appendChild(
                createElement(
                    "p",
                    "empty-message",
                    "У вас пока нет питомцев. Добавьте первого!"
                )
            );
        } else {
            pets.forEach(pet => {
                container.appendChild(createPetCard(pet));
            });
        }

        updatePetSelect();

    } catch (error) {
        container.textContent = error.message;
    }
}

function createPetCard(pet) {
    const card = createElement("article", "pet-card");

    const info = createElement("div", "pet-card-info");

    const avatar = createElement(
        "div",
        "pet-avatar",
        pet.species.toLowerCase().includes("кош") ? "🐱" : "🐶"
    );

    const description = createElement("div", "pet-description");

    description.appendChild(
        createElement("h3", "", pet.name)
    );

    description.appendChild(
        createElement(
            "p",
            "",
            `Вид: ${pet.species}`
        )
    );

    description.appendChild(
        createElement(
            "p",
            "",
            `Порода: ${pet.breed || "Не указана"}`
        )
    );

    description.appendChild(
        createElement(
            "p",
            "",
            `Дата рождения: ${formatDate(pet.birth_date)}`
        )
    );

    description.appendChild(
        createElement(
            "p",
            "",
            `Вес: ${pet.weight ?? "Не указан"} кг`
        )
    );

    description.appendChild(
        createElement(
            "p",
            "",
            pet.is_active ? "Статус: активен" : "Статус: неактивен"
        )
    );

    info.append(avatar, description);

    const actions = createElement("div", "pet-actions");

    const recordsButton = createElement(
        "button",
        "",
        "История"
    );

    recordsButton.type = "button";
    recordsButton.addEventListener("click", () => {
        loadHistory(pet.id);
        document.getElementById("history-section")
            .scrollIntoView({ behavior: "smooth" });
    });

    const deleteButton = createElement(
        "button",
        "",
        "Удалить"
    );

    deleteButton.type = "button";
    deleteButton.addEventListener("click", () => deletePet(pet.id));

    actions.append(recordsButton, deleteButton);
    card.append(info, actions);

    return card;
}

function updatePetSelect() {
    const select = document.getElementById("record-pet");

    select.replaceChildren();

    const firstOption = createElement(
        "option",
        "",
        pets.length ? "Выберите питомца" : "Сначала добавьте питомца"
    );

    firstOption.value = "";
    select.appendChild(firstOption);

    pets.forEach(pet => {
        const option = createElement("option", "", pet.name);
        option.value = pet.id;
        select.appendChild(option);
    });
}

document.getElementById("pet-form").addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        const data = {
            name: document.getElementById("pet-name").value.trim(),
            species: document.getElementById("pet-species").value.trim(),
            breed: document.getElementById("pet-breed").value.trim() || null,
            birth_date: document.getElementById("pet-birth-date").value || null,
            weight: document.getElementById("pet-weight").value
                ? Number(document.getElementById("pet-weight").value)
                : null,
            is_active: document.getElementById("pet-active").checked
        };

        try {
            await apiRequest("/api/pets/", {
                method: "POST",
                body: JSON.stringify(data)
            });

            showMessage("pet-message", "Питомец успешно добавлен!", true);

            event.target.reset();
            document.getElementById("pet-active").checked = true;

            await loadPets();

        } catch (error) {
            showMessage("pet-message", error.message);
        }
    }
);

async function deletePet(petId) {
    if (!confirm("Вы действительно хотите удалить питомца?")) {
        return;
    }

    try {
        await apiRequest(`/api/pets/${petId}`, {
            method: "DELETE"
        });

        await loadPets();
        await loadReminders();

    } catch (error) {
        alert(error.message);
    }
}

async function loadRecordTypes() {
    const select = document.getElementById("record-type");

    try {
        recordTypes = await apiRequest("/api/record-types/");

        select.replaceChildren();

        const firstOption = createElement(
            "option",
            "",
            "Выберите тип процедуры"
        );

        firstOption.value = "";
        select.appendChild(firstOption);

        recordTypes.forEach(type => {
            const option = createElement("option", "", type.name);
            option.value = type.id;
            select.appendChild(option);
        });

    } catch (error) {
        select.replaceChildren(
            createElement("option", "", "Не удалось загрузить типы")
        );
        console.error(error);
    }
}

document.getElementById("record-form").addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        const petId = document.getElementById("record-pet").value;

        if (!petId) {
            showMessage("record-message", "Сначала выберите питомца.");
            return;
        }

        const data = {
            record_type_id: Number(
                document.getElementById("record-type").value
            ),
            title: document.getElementById("record-title").value.trim(),
            record_date: document.getElementById("record-date").value,
            notes: document.getElementById("record-notes").value.trim() || null,
            completed: false
        };

        try {
            await apiRequest(`/api/pets/${petId}/records`, {
                method: "POST",
                body: JSON.stringify(data)
            });

            showMessage(
                "record-message",
                "Запись успешно сохранена!",
                true
            );

            event.target.reset();

            await loadHistory(petId);
            await loadReminders();

        } catch (error) {
            showMessage("record-message", error.message);
        }
    }
);

async function loadHistory(selectedPetId = null) {
    const container = document.getElementById("history-list");

    container.replaceChildren();

    const selectedPets = selectedPetId
        ? pets.filter(pet => pet.id === selectedPetId)
        : pets;

    if (selectedPets.length === 0) {
        container.appendChild(
            createElement("p", "empty-message", "Питомцев пока нет.")
        );
        return;
    }

    try {
        let records = [];

        for (const pet of selectedPets) {
            const petRecords = await apiRequest(
                `/api/pets/${pet.id}/records`
            );

            petRecords.forEach(record => {
                records.push({
                    ...record,
                    petName: pet.name
                });
            });
        }

        records.sort((a, b) =>
            b.record_date.localeCompare(a.record_date)
        );

        if (records.length === 0) {
            container.appendChild(
                createElement(
                    "p",
                    "empty-message",
                    "Ветеринарных записей пока нет."
                )
            );
            return;
        }

        records.forEach(record => {
            const item = createElement("article", "history-item");

            const marker = createElement("div", "history-marker");
            const content = createElement("div", "");

            const type = recordTypes.find(
                item => item.id === record.record_type_id
            );

            content.appendChild(
                createElement("h3", "", record.title)
            );

            content.appendChild(
                createElement(
                    "p",
                    "",
                    `${record.petName} · ${type?.name || "Процедура"}`
                )
            );

            content.appendChild(
                createElement(
                    "p",
                    "",
                    `Дата: ${formatDate(record.record_date)}`
                )
            );

            content.appendChild(
                createElement(
                    "p",
                    "",
                    record.completed ? "Выполнено" : "Не выполнено"
                )
            );

            if (record.notes) {
                content.appendChild(
                    createElement("p", "", record.notes)
                );
            }

            item.append(marker, content);
            container.appendChild(item);
        });

    } catch (error) {
        container.textContent = error.message;
    }
}

async function loadReminders() {
    const title = document.getElementById("reminder-title");
    const details = document.getElementById("reminder-details");

    try {
        const reminders = await apiRequest("/api/reminders/next");

        if (!reminders || reminders.length === 0) {
            title.textContent = "Пока нет ближайших напоминаний";
            details.textContent =
                "Здесь появятся запланированные ветеринарные процедуры.";
            return;
        }

        const reminder = reminders[0];

        title.textContent =
            reminder.title || "Предстоящая процедура";

        details.textContent =
            reminder.record_date
                ? `Дата: ${formatDate(reminder.record_date)}`
                : "Не забудьте позаботиться о питомце!";

    } catch (error) {
        title.textContent = "Не удалось загрузить напоминания";
        details.textContent = error.message;
    }
}

document.getElementById("logout-button").addEventListener(
    "click",
    async () => {
        try {
            await apiRequest("/api/auth/logout", {
                method: "POST"
            });

            window.location.href = "/login.html";

        } catch (error) {
            alert(error.message);
        }
    }
);

async function initApp() {
    try {
        await loadProfile();
        await loadPets();
        await loadRecordTypes();
        await loadHistory();
        await loadReminders();

    } catch (error) {
        console.error("Ошибка запуска PetPass:", error);
    }
}

initApp();

class ListManager {
    constructor(tableId) {
        // create the manager for the table
        this.tableElement = document.getElementById(tableId);
        if (!this.tableElement) {
            throw new Error(`Table with id ${tableId} not found`);
        }
        this.initializeEventListeners();
        console.log("listManager constructor");
    }

    initializeEventListeners() {
        // addEventListener(event type, (listener: type of thing happening => function to call))
        this.tableElement.addEventListener('click', (e) => this.handleClick(e));
        console.log("listManger initialized");
    }

    handleClick(e) {
        const target = e.target;
        // 3 equals signs? really?
        if (target && target.tagName === "BUTTON") {
            // tr being "table row", need it to update the UI later
            // closest selects the thing that matches the nearest ancestor
            const row = target.closest("tr");
            if (row) {
                const strEntryId = row.getAttribute("data-entry-id");
                if (strEntryId) {
                    console.log(`clicked, entry id ${strEntryId}`);
                    // where more button functionality will go if needed
                    const entryId = parseInt(strEntryId, 10);
                    if (target.classList.contains("mark-watched-btn")) {
                        this.sendRequest(`/entry/update/watched/${entryId}`, "POST", row, this.updateWatchedStatus);
                    }
                    else if (target.classList.contains("delete-btn")) {
                        this.sendRequest(`/entry/delete/${entryId}`, "POST", row, this.entryRowDelete);
                    }
                }
            }
        }
    }

    async sendRequest(url, method, row, successCallback) {
        try {
            // csrf token not implemented yet
            const response = await fetch(url, {method: method});
            // const response = await fetch(url, {method, headers:{
            //     "X-CSRFToken": this.getCSRFToken;
            // }})
            const data = await response.json();
            if (!response.ok || "error" in data) {
                throw new Error("Failed to send request");
            }
            successCallback(row);
        }
        catch (error) {
            console.error("Error:", error);
            // if it's an error type: display it, otherwise show the string
            alert(error instanceof Error ? error.message : "Error trying to send request");
        }
    }

    updateWatchedStatus(row) {
        const watchedCell = row.querySelector('.watched-status');
        const cellWatchedBtn = row.querySelector('.mark-watched-btn')
        if (watchedCell) {
            watchedCell.textContent = "Yes";
        }
        if (cellWatchedBtn) {
            cellWatchedBtn.remove();
        }
    }

    entryRowDelete(row) {
        row.remove();
    }
}

// Initialize the ListManager when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    new ListManager('watchlist-table');
});
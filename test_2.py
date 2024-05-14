row = table.currentRow()
if row != -1:
    bin_id = int(table.item(row, 0).text())
    response = QMessageBox.question(self, 'Confirm Deletion',
                                    "Are you sure you want to delete this item?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if response == QMessageBox.Yes:
        try:
            cursor.execute(
                "DELETE FROM bin_external WHERE bin_id = ?", (bin_id,))
            conn.commit()
            self.load_external_bin(self.exteranl_bin_table)
            QMessageBox.information(
                self, "Success", "Item has been deleted successfully.")
        except Exception as e:
            QMessageBox.warning(
                self, "Error", f"Failed to delete the item: {str(e)}")
    else:
        QMessageBox.information(
            self, "Cancelled", "Item deletion cancelled.")
else:
    QMessageBox.warning(self, "Selection Required",
                        "Please select an item to delete.")

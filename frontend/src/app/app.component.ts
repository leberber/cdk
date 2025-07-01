import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface Item {
  id?: number;
  name: string;
  description?: string;
}

@Component({
  selector: 'app-root',
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  title = 'Minimal FastAPI + Angular App';
  
  trackByItemId(index: number, item: Item): number {
    return item.id || index;
  }
  
  items: Item[] = [];
  newItem: Item = { name: '', description: '' };
  status = 'Ready';
  isLoading = false;

  // Use relative URL for CloudFront deployment
  // private apiUrl = '/api';
  
  // For local development, comment out above and use:
  private apiUrl = '/api';


  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadItems();
  }

  loadItems() {
    this.isLoading = true;
    this.status = 'Loading items...';
    
    this.http.get<Item[]>(`${this.apiUrl}/items`).subscribe({
      next: (data) => {
        this.items = data;
        this.status = `Loaded ${data.length} items successfully`;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error loading items:', error);
        this.status = 'Error loading items. Check if the backend is running.';
        this.isLoading = false;
      }
    });
  }

  addItem() {
    if (!this.newItem.name.trim()) {
      this.status = 'Please enter an item name';
      return;
    }

    this.isLoading = true;
    this.status = 'Adding item...';
    
    this.http.post<Item>(`${this.apiUrl}/items`, this.newItem).subscribe({
      next: (item) => {
        this.items.push(item);
        this.newItem = { name: '', description: '' };
        this.status = `Item "${item.name}" added successfully!`;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error adding item:', error);
        this.status = 'Error adding item. Please try again.';
        this.isLoading = false;
      }
    });
  }

  deleteItem(id: number, name: string) {
    if (!confirm(`Are you sure you want to delete "${name}"?`)) {
      return;
    }

    this.isLoading = true;
    this.status = 'Deleting item...';
    
    this.http.delete(`${this.apiUrl}/items/${id}`).subscribe({
      next: () => {
        this.items = this.items.filter(item => item.id !== id);
        this.status = `Item "${name}" deleted successfully!`;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error deleting item:', error);
        this.status = 'Error deleting item. Please try again.';
        this.isLoading = false;
      }
    });
  }

  refresh() {
    this.loadItems();
  }
}
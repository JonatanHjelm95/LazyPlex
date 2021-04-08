import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import {environment} from '../../environments/environment'

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {
  shown: boolean = false
  path: string
  constructor(private http: HttpClient) { }
  url: string = environment.baseURL;

  ngOnInit(): void {
    this.getApplicationPath();
  }

  getApplicationPath(){
    this.http.get(this.url+'path').subscribe(data => {
      this.path = data['path']
     })
  }

  toggleSidebar(){
    this.shown = !this.shown
    this.getApplicationPath();

  }

  onSubmit(path){
    let data = {path:path.name}
    this.http.post('http://127.0.0.1:5000/setpath', data).subscribe(res => {
    })
  }
}

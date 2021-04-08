import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Downloads } from '../downloads'
import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';
import {environment} from '../../environments/environment'

@Component({
  selector: 'app-bottombar',
  templateUrl: './bottombar.component.html',
  styleUrls: ['./bottombar.component.css'],
})
export class BottombarComponent implements OnInit {
  closeResult = '';
  origin_title: string = '';
  activeDownloads: Downloads[] = []
  url: string = environment.baseURL;
  constructor(private http: HttpClient, private modalService: NgbModal) { }

  ngOnInit() {
    this.getTorrentInfo()
    setInterval(() => {
      this.getTorrentInfo()
    }, 5000)
  }

  getTorrentInfo() {
    this.http.get<any>(this.url + 'torrents').subscribe(res => {
      this.activeDownloads = res
    })
  }

  controlqtClient(control){
    let data = {control:control}
    this.http.post<any>(this.url+'control',data).subscribe(res => {
      //console.log(res)
    })
  }

  getOriginTitle(title){
    let data = {title: title}
    console.log(data)
    this.http.post<any>(this.url+'title', data).subscribe(res => {
      this.origin_title = res
    })
  }

  open(content, title) {
    this.getOriginTitle(title)
    this.modalService.open(content, {ariaLabelledBy: 'modal-basic-title'}).result.then((result) => {
      this.closeResult = `Closed with: ${result}`;
    }, (reason) => {
      this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
    });
  }

  onSubmit(origin_title, title){
    let data = {origin_title:origin_title['name'], title:title}
    console.log(data)
    this.http.post<any>(this.url+'settitle', data).subscribe(res => {
      this.modalService.dismissAll()
    })

  }

  private getDismissReason(reason: any): string {
    if (reason === ModalDismissReasons.ESC) {
      return 'by pressing ESC';
    } else if (reason === ModalDismissReasons.BACKDROP_CLICK) {
      return 'by clicking on a backdrop';
    } else {
      return `with: ${reason}`;
    }
  }
}

import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Torrent } from '../torrent';
import {NgxPaginationModule} from 'ngx-pagination'; // <-- import the module
import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';
import {environment} from '../../environments/environment'


@Component({
  selector: 'app-torrent-lookup',
  templateUrl: './torrent-lookup.component.html',
  styleUrls: ['./torrent-lookup.component.css']
})
export class TorrentLookupComponent implements OnInit {
  torrents : Torrent[]
  p: number = 1
  closeResult = '';
  originName: string = ''

  ngOnInit(): void {
  }

  constructor(private http: HttpClient, private modalService: NgbModal) { }
  url: string = environment.baseURL;
  onSubmit(data) {
    this.originName = data['name']
    this.torrents = []
    this.http.post<any>(this.url+'lookup', data)
    .subscribe(data => this.torrents = data)

  }
  downloadTorrent(torrent: Torrent){
    const order = {origin_title: this.originName, title: torrent.name, magnet: torrent.magnet, status: 'active'}
    console.log(order)
    this.http.post<any>(this.url+'download', order)
    .subscribe(data => this.modalService.dismissAll())

    //this.open(content, torrent)
    //console.log(magnet)
  }
  
  open(content) {
    this.modalService.open(content, {ariaLabelledBy: 'modal-basic-title'}).result.then((result) => {
      this.closeResult = `Closed with: ${result}`;
    }, (reason) => {
      this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
    });
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

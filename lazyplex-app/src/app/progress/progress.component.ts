import { Component, Input, OnInit } from '@angular/core';
import { reduceEachTrailingCommentRange } from 'typescript';
import { Downloads } from '../downloads';

@Component({
  selector: 'app-progress',
  templateUrl: './progress.component.html',
  styleUrls: ['./progress.component.css']
})
export class ProgressComponent implements OnInit {
  @Input() download: Downloads
  progressPct: number
  progressColor: String = 'red'
  constructor() { }

  ngOnInit(): void {
    this.setProgress(this.download)
  }

  setProgress(download: Downloads){
    this.progressPct = download.progress*100
    this.progressColor = this.setProgressColor(download.speed)
  }

  setProgressColor(speed){
    if(parseInt(speed.split('.')[0]) == 0){
      return 'red'
    }
    else return speed.includes('MB') ? 'green' : 'orange'
  }


}

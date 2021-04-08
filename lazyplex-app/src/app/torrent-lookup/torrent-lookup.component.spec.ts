import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TorrentLookupComponent } from './torrent-lookup.component';

describe('TorrentLookupComponent', () => {
  let component: TorrentLookupComponent;
  let fixture: ComponentFixture<TorrentLookupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TorrentLookupComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TorrentLookupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import scrapy
from .config_loader import test_config
import re



class OpSpider(scrapy.Spider):
    name = "ashimGandu"
    start_urls = [test_config()['target_url']]

    def parse(self, response):
        manga_chaps=response.css('.wp-manga-chapter')
        
        if not manga_chaps:
            self.logger.warning("No manga chapter found on page")
            return
        
        if manga_chaps:
            try:
                for chaps_links in manga_chaps:
                    chaps_a_links=chaps_links.css('a').attrib['href']
                    chap_number=chaps_links.css('a::text').get().strip().split('Chapter ')[1].split(' ')[0]
                    chap_number=float(re.search(r'\d+(\.\d+)?',chap_number).group())
                    yield scrapy.Request(url=chaps_a_links,meta={'chapter_number': chap_number},callback=self.image_parse)
                    
                    
            except Exception as e:
                self.logger.error(f"Error processing chapter: {str(e)}")
        
    
    def image_parse(self,response):
        image_files=[]
        chapter_number=response.meta.get('chapter_number')
        chapter_key = str(chapter_number)
        if(chapter_key.find('.')):
            chapter_key=chapter_key.replace('.','_')
            
        chaps_images=response.css('.wp-manga-chapter-img')
        for chap_img in chaps_images:
            try:
                image_link=chap_img.attrib['src'].strip()
                image_files.append(image_link)
            except KeyError:
                self.logger.warning("Could not find src attribute for image in chapter")
            
        yield{
            chapter_key:image_files
        }
        
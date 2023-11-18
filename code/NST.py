from cyt_dataloader import PairedDataset, DataLoader
from Encoder import Lora_Encoder
from zyj_decode import Decoder

batch_size = 4
content_dir = "C:/Users/ZhouXunZhe/Desktop/NST_subset/content"
style_dir = "C:/Users/ZhouXunZhe/Desktop/NST_subset/style"

train_dataset = PairedDataset(content_dir, style_dir, crop = False, norm = False, mode='train')
train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)


class NST:
    def __init__(self, encoder_num_layers=6, decoder_num_layers=3):
        self.encoder_num_layers = encoder_num_layers
        self.encoder_c = Lora_Encoder(self.encoder_num_layers)
        self.encoder_s = Lora_Encoder(self.encoder_num_layers)

        self.decoder = Decoder(trans_decoder_layers_num=decoder_num_layers)

    def forward(self, content_image, style_image):
        content, content_pos = self.encoder_c.forward(content_image)
        style, _ = self.encoder_s.forward(style_image)
        
        output = self.decoder(content, style, content_pos)

        return output


# Test for demo images
My_NST = NST(6)

for content_image, style_image in train_dataloader:
    output = My_NST.forward(content_image, style_image)
    print(output.shape)
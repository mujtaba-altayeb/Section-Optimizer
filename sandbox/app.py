import sectiondesigner as sd

ga = sd.GA(4, 5, 9, 40, b_range=[270, 280], h_range=[370, 380])
best, designs = ga.RunGA()

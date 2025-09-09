---
############################### Banner ##############################
banner:
  enable: true
  bg_image: "images/slider-bg.jpg"
  bg_overlay: true
  title: "Dominique Schr&ouml;der <br/> "
  content: "Professor of Privacy Enhancing Technologies"

############################# About #################################
about:
  enable: true
  title: "About Me"
  description: ""
  content: "
  content: "I am a full professor of Privacy-Enhancing Technologies at TU Wien. My research aims to make security a design property — specified, verified, and certifiable — rather than an afterthought tested by audits. <br/><br/> I work at the intersection of cryptography, formal methods, and systems, with the goal of building infrastructures that are both innovative and trustworthy. My contributions span from password-hardened encryption and privacy-preserving analytics, to secure ledgers and messaging protocols, to automated tools for formal certification.  <br/><br/> At stake is not only technical correctness but societal legitimacy: citizens must trust that their data is safe, that services will not collapse under attack, and that privacy is a guarantee, not a luxury.</br></br>"

  **E-Mail: schroeder AA@TT me.com (replace AA@TT by @)**
 "
  button:
    enable: true
    label: "Discover Our Project"
    link: "project/"

  image: "images/Dominique-Schroeder.jpg"

######################### Research and Teaching ###############################
research:
  bg_image: "images/bg-gray.jpg"
  title: "Research Interests"
  content: "I am broadly interested in various topics across cryptography and its intersections with related areas such as privacy, theory, and formal methods. I'm passionate about the development of privacy-preserving techniques that have the potential to enhance security and privacy in practice. "
  content2: "I love interacting with young and highly motivated people wishing to gain a deeper understanding. My goal as a teacher is the creating an environment where we jointly explore a topic, where everyone helps each other, and where mistakes are not a problem but a helpful element to understanding a subject better.  "
  enable : true
  tabs:
  # tab item loop
  - name : "Privacy"
    content : "New technology and the possibilities that arise from it excite me. 
Some years ago, the Economist wrote, *''The world's most valuable resource is no longer oil, but data.''* The high value of data has enabled companies like Alphabet to become one of the world's largest and most influential companies. The digitalization and networking of all data are also making inroads in medicine; various countries recently passed laws on the (scientific) use of data. I am fascinated by the possibilities that can arise by linking data and (automated) machine analysis. My research supports this development by enabling modern applications in a privacy-preserving way. I am investigating the combination of modern cryptographic techniques, such as homomorphic cryptography and secure multiparty computation, with differential privacy techniques. The goal is to realize the same functionality of new applications without compromising the individual's privacy. "

  - name : "Distributed Trust"
    content : "I am excited by the development of practical decentralized cryptographic systems whose security does not rely on trusted parties. The practical development of these systems goes hand in hand with technological advances in modern communication systems and networks. Unlike centralized systems, the security of a system relies on honest majority assumptions in contrast to a single trusted party. One of the most prominent examples are modern cryptocurrencies, such as Bitcoin. In this area, I am particularly interested in privacy-preserving cryptocurrencies and techniques to (secure) enhance the efficiency of distributed systems. "

  - name : "Privacy-Preserving Technologies"
    content : "Cryptographers have developed a beautiful landscape of exciting primitives that enhance privacy. The primitive include advanced signature schemes, such as ring signatures, group signatures, sanitizable signatures, functional commitments, and oblivious (group) ORAM, to name a few. I like the richness of the schemes, the beauty of the constructions, and also the potential to be used in practice. With my research, I contributed to developing these primitives in terms of understanding the underlying security notions and the development of practical schemes. "

  - name : "Low Entropy"
    content : "The security of most cryptographic systems relies on perfect conditions, such as uniform random keys and ideal randomness. But the reality is often very different as cryptographic keys are derived from low entropy sources, such as passwords, fingerprints, face recognition, etc. The same holds for randomness, which is computed from (weak) pseudorandom generators. Most cryptographic schemes are insecure if one or both ingredients do not satisfy the underlying requirements. I enjoy exploring the boundaries of practical cryptographic systems where weak sources of secrets and randomness are used, with the hope of bridging the practice and theory of cryptography. "    

  - name : "Idealized Models"
    content : "The security of many practical cryptographic schemes relies on idealized models, such as the random oracle model or the common reference string model. The basic idea of these models is to heuristically treat one or more of the building blocks as an ''ideal'' object. While proofs without these idealized models are preferable, they help us learn a lot about the security of practical schemes. I enjoy working in this area as the results impact theory and practice. On the one hand, we learn about the difficulty of realizing cryptographic tasks. On the other hand, we can gain confidence in schemes used in practice."


#########################  Teaching ###############################
teaching:
  bg_image: "images/bg-light-gray.jpg"
  title: "Teaching Activities"
  content: "I love interacting with young and highly motivated people wishing to gain a deeper understanding. My goal as a teacher is the creating an environment where we jointly explore a topic, where everyone helps each other, and where mistakes are not a problem but a helpful element to understanding a subject better.  "
  enable : true
  tabs:
  - name : "Crypto"   
    content : "lsd;lfs;'dlfd brasdds rLorem ipsum dolor sit amet, consectetur adipisicing elit. Inventore nobis ducimus facere repellat
    harum, eius cupiditate, aliquam aut deserunt. Nemo illo ex impedit autem quod nobis architecto, velit
    quasi, aut voluptas porro natus. Fuga magnam perspiciatis fugit, placeat possimus officia non ducimus
    voluptatum aspernatur ad quidem neque accusantium repudiandae cupiditate nobis corporis, cum facere
    iusto, modi cumque consectetur saepe. Officia, molestiae tempore! Consequatur ipsa consequuntur saepe
    suscipit vero laudantium, mollitia, quaerat soluta nihil non tempore, quos dignissimos quasi ab officiis
    illum numquam quibusdam ducimus, veritatis ad. Quia, aliquid. Quaerat quos ducimus ipsam amet minus
    temporibus eos sequi alias hic nemo."
    
  - name : "Data Privacy"   
    content : "veritatis ad. Quia, aliquid. Quaerat quos ducimus ipsam amet minus
    temporibus eos sequi alias hic nemo."

  - name : "Cryptocurrencies"   
    content : "lsd;lfs;'dlfd brasdds rLorem ipsum dolor sit amet, consectetur adipisicing elit. Inventore nobis ducimus facere repellat
    harum, eius cupiditate, aliquam aut deserunt. Nemo illo ex impedit autem quod nobis architecto, velit
    quasi, aut voluptas porro natus. Fuga magnam perspiciatis fugit, placeat possimus officia non ducimus
    voluptatum aspernatur ad quidem neque accusantium repudiandae cupiditate nobis corporis, cum facere
    iusto, modi cumque consectetur saepe. Officia, molestiae tempore! Consequatur ipsa consequuntur saepe
    suscipit vero laudantium, mollitia, quaerat soluta nihil non tempore, quos dignissimos quasi ab officiis
    illum numquam quibusdam ducimus, veritatis ad. Quia, aliquid. Quaerat quos ducimus ipsam amet minus
    temporibus eos sequi alias hic nemo."

  - name : "Algorithms"   
    content : "rLorem ipsum dolor sit amet, consectetur adipisicing elit. Inventore nobis ducimus facere repellat
    harum, eius cupiditate, aliquam aut deserunt. Nemo illo ex impedit autem quod nobis architecto, velit
    quasi, aut voluptas porro natus. Fuga magnam perspiciatis fugit, placeat possimus officia non ducimus
    voluptatum aspernatur ad qu"

######################### Recent Publications ###############################
publications:
  title: "Recent publications"
  description: "Summmary of my recent publications"
  content: "none"
  enable: true

  ############################# Activities ############################
activities:
  bg_image: "images/bg-gray.jpg"
  title: Recent Activities and Community Services 
  enable: true
  # students content comes from "students.md" file
  tabs:
    - name : "PC Memberships"
      content : "I regularly serve on the leading cryptography and IT security conferences PCs, such as CRYPTO'23, EUROCRYPT'23, ACM CCS'23."

    - name : "Reviews for Funding Agencies"
      content : "The review of research proposals is also part of my activities, such as the ERC, DFG, and FWF."

    - name : "Department Service"
      content : "I also contribute to academic self-governance as an elected member of the Faculty Council, Deputy Speaker of the Department of Computer Science in the NCT, and the study committee for the part-time Bachelor of IT Security. "
    

---
